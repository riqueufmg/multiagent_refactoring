import json
import shutil
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from mvp.planner.lib.fqn import Fqn
from mvp.planner.lib.file_system import FileSystem
from mvp.planner.lib.config_utils import load_config, require_config_value
from mvp.planner.lib.designite_utils import (
    _run_designite,
    _designite_smell_present,
    get_package_dependencies,
)
from mvp.planner.lib.json_utils import _extract_json_object_only
from mvp.planner.lib.path_utils import (
    _read_target_file,
    _extract_fqn_from_java,
    _infer_source_root_from_target,
    _infer_target_type_from_name,
)
from mvp.planner.lib.java_context import extract_observed_external_calls
from mvp.planner.lib.plan_utils import (
    enrich_plan_with_visibility_ops,
    enrich_plan_with_related_tests,
)
from mvp.planner.state import PlannerState


def _cfg(state: PlannerState, dotted_key: str, default: Any = None) -> Any:
    current: Any = state.get("config") or {}

    for part in dotted_key.split("."):
        if not isinstance(current, dict) or part not in current:
            return default
        current = current[part]

    return current


def load_config_node(state: PlannerState) -> PlannerState:
    cfg = load_config(state["config_path"])

    state["config"] = cfg
    state["project_name"] = str(require_config_value(cfg, "project.name"))
    repo_path = _require_absolute_path(
    str(require_config_value(cfg, "project.repo_path")),
        "project.repo_path",
    )

    if not repo_path.exists() or not repo_path.is_dir():
        raise RuntimeError(f"project.repo_path not found or not a directory: {repo_path}")

    state["repo_path"] = str(repo_path)
    state["project_root"] = str(Path.cwd().resolve())

    state["smell"] = str(require_config_value(cfg, "target.smell")).strip()
    state["smell_name"] = str(require_config_value(cfg, "target.smell_name")).strip()
    state["target_name"] = str(require_config_value(cfg, "target.target_name")).strip()
    state["target_type"] = str(
        cfg.get("target", {}).get("target_type")
        or _infer_target_type_from_name(state["target_name"])
    ).strip()

    state["designite_smells_csv"] = str(require_config_value(cfg, "designite.smells_csv"))

    system_prompt_path = _require_absolute_path(
        str(require_config_value(cfg, "prompts.system")),
        "prompts.system",
    )
    smell_prompt_path = _require_absolute_path(
        str(require_config_value(cfg, "prompts.smell")),
        "prompts.smell",
    )

    if not system_prompt_path.exists():
        raise RuntimeError(f"System prompt not found: {system_prompt_path}")

    if not smell_prompt_path.exists():
        raise RuntimeError(f"Smell prompt not found: {smell_prompt_path}")

    state["planner_system_prompt_path"] = str(system_prompt_path)
    state["planner_smell_prompt_path"] = str(smell_prompt_path)

    return state

def _require_absolute_path(value: str, field_name: str) -> Path:
    path = Path(value).expanduser()

    if not path.is_absolute():
        raise ValueError(f"{field_name} must be an absolute path: {value}")

    return path.resolve()

def init_run_node(state: PlannerState) -> PlannerState:
    cfg = state["config"]

    runs_dir_cfg = str(require_config_value(cfg, "output.runs_dir"))
    runs_dir = _require_absolute_path(runs_dir_cfg, "output.runs_dir")
    runs_dir.mkdir(parents=True, exist_ok=True)

    run_id_cfg = cfg.get("mvp", {}).get("run_id", "auto")

    if run_id_cfg and run_id_cfg != "auto":
        run_id = str(run_id_cfg)
    else:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        rid = uuid.uuid4().hex[:8]
        run_id = f"{ts}_{rid}"

    run_dir = runs_dir / run_id
    planner_dir = run_dir / "planner"
    planner_dir.mkdir(parents=True, exist_ok=True)

    state["run_id"] = run_id
    state["run_dir"] = str(run_dir)
    state["planner_dir"] = str(planner_dir)

    shutil.copyfile(state["config_path"], planner_dir / "config.snapshot.yml")

    return state


def resolve_target_node(state: PlannerState) -> PlannerState:
    repo_path = Path(state["repo_path"]).resolve()
    target_name = state["target_name"]
    target_type = state["target_type"]

    target_path = Fqn(target_name).find_in_repo(repo_path)

    if target_path is None:
        raise RuntimeError(f"Target not found: {target_name}")

    if target_type == "class":
        if not target_path.is_file():
            raise RuntimeError(f"Class target must resolve to a file: {target_path}")

        target_file = str(target_path.relative_to(repo_path)).replace("\\", "/")
        target_rel, target_code = _read_target_file(repo_path, target_file)

        target_fqn = _extract_fqn_from_java(target_code, target_rel)
        source_root = _infer_source_root_from_target(repo_path, target_rel, target_fqn)

        state["target_file"] = target_rel
        state["target_code"] = target_code
        state["target_class_fqn"] = target_fqn
        state["target_source_root"] = source_root

    elif target_type == "package":
        if not target_path.is_dir():
            raise RuntimeError(f"Package target must resolve to a directory: {target_path}")

        target_files = FileSystem(str(repo_path), str(target_path)).list_java_files_in_dir()

        if not target_files:
            raise RuntimeError(f"Package target has no Java files: {target_name}")

        source_root_path = target_path.resolve()
        for _ in target_name.split("."):
            source_root_path = source_root_path.parent

        state["target_files"] = target_files
        state["target_source_root"] = str(
            source_root_path.relative_to(repo_path)
        ).replace("\\", "/")

    else:
        raise RuntimeError(f"Unsupported target_type: {target_type}")

    planner_dir = Path(state["planner_dir"])
    (planner_dir / "target.json").write_text(
        json.dumps(
            {
                "target_type": state["target_type"],
                "target_name": state["target_name"],
                "target_file": state.get("target_file", ""),
                "target_files": state.get("target_files", []),
                "target_source_root": state.get("target_source_root", ""),
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    return state


def run_designite_node(state: PlannerState) -> PlannerState:
    repo_path = Path(state["repo_path"]).resolve()
    planner_dir = Path(state["planner_dir"])

    jar_cfg = _cfg(state, "designite.jar_path")
    if not jar_cfg:
        raise RuntimeError("designite.jar_path is missing")

    designite_jar = _require_absolute_path(str(jar_cfg), "designite.jar_path")

    if not designite_jar.exists() or not designite_jar.is_file():
        raise RuntimeError(f"Designite JAR not found: {designite_jar}")

    java_path = _cfg(state, "designite.java_path", "java")

    designite_dir = planner_dir / "designite"
    designite_dir.mkdir(parents=True, exist_ok=True)

    out_dir, cmd = _run_designite(
        repo_path=repo_path,
        output_root=designite_dir,
        designite_jar=designite_jar,
        java_path=java_path,
    )

    state["designite_dir"] = str(out_dir)

    (planner_dir / "designite.status.json").write_text(
        json.dumps(
            {
                "ok": True,
                "designite_dir": str(out_dir),
                "cmd": cmd,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    return state


def check_smell_node(state: PlannerState) -> PlannerState:
    designite_dir = Path(state["designite_dir"])
    target_type = state["target_type"]

    if target_type == "package":
        designite_target = state["target_name"]
    else:
        designite_target = state.get("target_class_fqn", state["target_name"])

    present = _designite_smell_present(
        designite_dir=designite_dir,
        target_name=designite_target,
        smell_name=state["smell_name"],
        csv_name=state["designite_smells_csv"],
        target_type=target_type,
    )

    state["target_has_smell"] = bool(present)

    planner_dir = Path(state["planner_dir"])
    (planner_dir / "smell_check.json").write_text(
        json.dumps(
            {
                "target_has_smell": state["target_has_smell"],
                "target": designite_target,
                "smell_name": state["smell_name"],
                "csv": state["designite_smells_csv"],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    if not state["target_has_smell"]:
        state["stop_reason"] = "target_without_smell"

    return state


def after_check_smell(state: PlannerState) -> str:
    if state.get("target_has_smell"):
        return "build_planner_context"
    return "save_status"


def build_planner_context_node(state: PlannerState) -> PlannerState:
    smell = state["smell"]
    target_type = state["target_type"]

    planner_input: dict[str, Any] = {
        "smell": state["smell_name"],
        "target_type": target_type,
        "target_name": state["target_name"],
        "designite": {
            "dir": state["designite_dir"],
            "smells_csv": state["designite_smells_csv"],
            "target_has_smell": state["target_has_smell"],
        },
    }

    if target_type == "class":
        planner_input.update(
            {
                "target_file": state["target_file"],
                "target_source_root": state["target_source_root"],
                "target_code": state["target_code"],
            }
        )

        if smell == "HM":
            planner_input["observed_external_calls"] = extract_observed_external_calls(
                state["target_code"]
            )

    elif target_type == "package":
        planner_input.update(
            {
                "target_source_root": state["target_source_root"],
                "target_files": state["target_files"],
            }
        )

        if smell == "GC":
            graphml_path = Path(state["designite_dir"]) / "DependencyGraph.graphml"
            internal_deps, outgoing_deps, incoming_deps = get_package_dependencies(
                graphml_path,
                state["target_name"],
            )

            planner_input["internal_deps"] = internal_deps
            planner_input["incoming_deps"] = incoming_deps
            planner_input["outgoing_deps"] = outgoing_deps

    else:
        raise RuntimeError(f"Unsupported target_type: {target_type}")

    state["planner_input"] = planner_input
    state["planner_input_json"] = json.dumps(planner_input, indent=2)

    planner_dir = Path(state["planner_dir"])
    (planner_dir / "planner.input.json").write_text(
        state["planner_input_json"],
        encoding="utf-8",
    )

    return state


def call_planner_node(state: PlannerState) -> PlannerState:
    planner_dir = Path(state["planner_dir"])

    system_prompt = Path(state["planner_system_prompt_path"]).read_text(encoding="utf-8")
    smell_prompt = Path(state["planner_smell_prompt_path"]).read_text(encoding="utf-8")

    rendered = smell_prompt.replace("{input}", state["planner_input_json"])

    state["planner_system_prompt"] = system_prompt
    state["planner_smell_prompt"] = smell_prompt
    state["planner_rendered_prompt"] = rendered

    (planner_dir / "system.prompt").write_text(system_prompt, encoding="utf-8")
    (planner_dir / "smell.prompt").write_text(smell_prompt, encoding="utf-8")
    (planner_dir / "planner.rendered.md").write_text(rendered, encoding="utf-8")

    model = _cfg(state, "models.planner", "gpt-5-mini")
    temperature = float(_cfg(state, "planner.temperature", 0.0))
    timeout = int(_cfg(state, "planner.timeout", 120))
    max_retries = int(_cfg(state, "planner.max_retries", 2))

    ## model object instance
    llm = ChatOpenAI(
        model=model,
        temperature=temperature,
        timeout=timeout,
        max_retries=max_retries,
    )

    ## model's inference
    res = llm.invoke(
        [
            SystemMessage(content=system_prompt),
            HumanMessage(content=rendered),
        ]
    )

    raw = (res.content or "").strip()
    state["planner_raw"] = raw

    (planner_dir / "planner.raw.txt").write_text(raw, encoding="utf-8")

    try:
        json_text = _extract_json_object_only(raw)
        plan = json.loads(json_text)

        (planner_dir / "plan.raw.json").write_text(
            json.dumps(plan, indent=2),
            encoding="utf-8",
        )

        planner_input = state.get("planner_input", {})

        ## plan's mechanical enrichment to UPDATE_VISIBILITY when MOVE_CLASS
        ## exists in the plan
        if (
            state.get("target_type") == "package"
            and state.get("smell_name") == "God Component"
        ):
            plan = enrich_plan_with_visibility_ops(
                plan,
                {
                    "internal_deps": planner_input.get("internal_deps", []),
                    "target_files": planner_input.get("target_files", []),
                    "target_source_root": planner_input.get("target_source_root", ""),
                },
            )

            (planner_dir / "plan.enriched.json").write_text(
                json.dumps(plan, indent=2),
                encoding="utf-8",
            )
        
        ## enrich plan with UPDATE_TESTS
        plan = enrich_plan_with_related_tests(
            plan,
            {
                "repo_path": state.get("repo_path", ""),
                "target_source_root": planner_input.get(
                    "target_source_root",
                    state.get("target_source_root", ""),
                ),
            },
        )

        (planner_dir / "plan.enriched.tests.json").write_text(
            json.dumps(plan, indent=2),
            encoding="utf-8",
        )

        state["plan"] = plan
        state["plan_ok"] = True
        state["plan_error"] = ""

        (planner_dir / "plan.json").write_text(
            json.dumps(plan, indent=2),
            encoding="utf-8",
        )

    except Exception as e:
        state["plan"] = {}
        state["plan_ok"] = False
        state["plan_error"] = str(e)

    return state


def validate_plan_node(state: PlannerState) -> PlannerState:
    planner_dir = Path(state["planner_dir"])

    if not state.get("plan_ok"):
        return state

    try:
        plan = state["plan"]

        if not isinstance(plan, dict):
            raise ValueError("plan must be a JSON object")

        if "blocks" not in plan:
            raise ValueError("plan missing required key: blocks")

        if not isinstance(plan["blocks"], list):
            raise ValueError("plan.blocks must be a list")

        for i, block in enumerate(plan["blocks"]):
            if not isinstance(block, dict):
                raise ValueError(f"block {i} must be an object")

            for key in ["id", "goal", "files", "ops"]:
                if key not in block:
                    raise ValueError(f"block {i} missing key: {key}")

        state["plan_ok"] = True
        state["plan_error"] = ""

        (planner_dir / "plan.validated.json").write_text(
            json.dumps(state["plan"], indent=2),
            encoding="utf-8",
        )

    except Exception as e:
        state["plan_ok"] = False
        state["plan_error"] = str(e)

    (planner_dir / "plan.validation.json").write_text(
        json.dumps(
            {
                "plan_ok": state.get("plan_ok", False),
                "plan_error": state.get("plan_error", ""),
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    return state


def save_status_node(state: PlannerState) -> PlannerState:
    planner_dir = Path(state["planner_dir"])

    ok = bool(state.get("target_has_smell")) and bool(state.get("plan_ok"))

    status = {
        "mvp": "planner",
        "ok": ok,
        "run_id": state.get("run_id", ""),
        "project": state.get("project_name", ""),
        "repo_path": state.get("repo_path", ""),
        "smell": state.get("smell", ""),
        "smell_name": state.get("smell_name", ""),
        "target_type": state.get("target_type", ""),
        "target_name": state.get("target_name", ""),
        "target_has_smell": state.get("target_has_smell", False),
        "plan_ok": state.get("plan_ok", False),
        "plan_error": state.get("plan_error", ""),
        "stop_reason": state.get("stop_reason", ""),
    }

    contract = {
        "producer": "planner",
        "version": "1.0",
        "ok": ok,
        "run_id": state.get("run_id", ""),
        "project": {
            "name": state.get("project_name", ""),
            "repo_path": state.get("repo_path", ""),
        },
        "target": {
            "smell": state.get("smell", ""),
            "smell_name": state.get("smell_name", ""),
            "target_type": state.get("target_type", ""),
            "target_name": state.get("target_name", ""),
            "target_file": state.get("target_file", ""),
            "target_files": state.get("target_files", []),
            "target_source_root": state.get("target_source_root", ""),
        },
        "artifacts": {
            "planner_dir": str(planner_dir),
            "plan": str(planner_dir / "plan.json"),
            "planner_input": str(planner_dir / "planner.input.json"),
            "designite_dir": state.get("designite_dir", ""),
            "status": str(planner_dir / "status.json"),
        },
    }

    state["status"] = status
    state["contract"] = contract

    (planner_dir / "status.json").write_text(
        json.dumps(status, indent=2),
        encoding="utf-8",
    )
    (planner_dir / "contract.json").write_text(
        json.dumps(contract, indent=2),
        encoding="utf-8",
    )

    return state