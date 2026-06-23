from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict):
        raise RuntimeError(f"Invalid YAML config: {path}")

    return data


def write_yaml(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(
            data,
            f,
            sort_keys=False,
            allow_unicode=True,
        )


def read_json_if_exists(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None

    if not isinstance(data, dict):
        return None

    return data


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", errors="replace")


def require(cfg: dict[str, Any], dotted_key: str) -> Any:
    current: Any = cfg

    for part in dotted_key.split("."):
        if not isinstance(current, dict) or part not in current:
            raise RuntimeError(f"Missing config key: {dotted_key}")
        current = current[part]

    return current


def sanitize_target_name(target_name: str) -> str:
    value = re.sub(r"[^A-Za-z0-9]+", "_", target_name)
    value = re.sub(r"_+", "_", value).strip("_")
    return value


def instance_dir_name(smell: str, target_name: str) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    target_slug = sanitize_target_name(target_name)
    return f"{timestamp}_{smell}__{target_slug}"


def set_common_mvp_config(
    base_cfg: dict[str, Any],
    orchestrator_cfg: dict[str, Any],
    instance_dir: Path,
    run_id: str,
) -> dict[str, Any]:
    cfg = deepcopy(base_cfg)

    cfg.setdefault("mvp", {})
    cfg["mvp"]["run_id"] = run_id

    cfg.setdefault("project", {})
    cfg["project"]["name"] = require(orchestrator_cfg, "project.name")
    cfg["project"]["repo_path"] = require(orchestrator_cfg, "project.repo_path")

    cfg.setdefault("target", {})
    cfg["target"]["smell"] = require(orchestrator_cfg, "target.smell")
    cfg["target"]["smell_name"] = require(orchestrator_cfg, "target.smell_name")
    cfg["target"]["target_type"] = require(orchestrator_cfg, "target.target_type")
    cfg["target"]["target_name"] = require(orchestrator_cfg, "target.target_name")

    cfg.setdefault("output", {})
    cfg["output"]["runs_dir"] = str(instance_dir)

    return cfg


def set_planner_contract_path(
    source_cfg: dict[str, Any],
    contract_path: Path,
) -> dict[str, Any]:
    cfg = deepcopy(source_cfg)
    contract = str(contract_path)

    # Main expected locations.
    cfg.setdefault("input", {})
    cfg["input"]["planner_contract"] = contract
    cfg["input"]["planner_contract_path"] = contract

    # Extra aliases. They are harmless if ignored by the MVP.
    cfg["planner_contract"] = contract
    cfg["planner_contract_path"] = contract

    cfg.setdefault("planner", {})
    cfg["planner"]["contract"] = contract
    cfg["planner"]["contract_path"] = contract

    return cfg


def run_command(
    cmd: list[str],
    cwd: Path,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(cwd),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def write_stop_file(
    instance_dir: Path,
    reason: str,
    run_id: str,
    details: dict[str, Any] | None = None,
) -> None:
    payload: dict[str, Any] = {
        "stop_reason": reason,
        "stopped_at_run": run_id,
    }

    if details:
        payload["details"] = details

    write_json(instance_dir / "stop.json", payload)


def detect_planner_stop_reason(
    contract_path: Path,
    status_path: Path,
) -> tuple[str | None, dict[str, Any]]:
    contract = read_json_if_exists(contract_path)
    status = read_json_if_exists(status_path)

    details: dict[str, Any] = {
        "contract_path": str(contract_path),
        "status_path": str(status_path),
        "contract_exists": contract_path.exists(),
        "status_exists": status_path.exists(),
        "contract": contract or {},
        "status": status or {},
    }

    if contract is None:
        return "planner_contract_not_found", details

    contract_ok = bool(contract.get("ok", False))

    if contract_ok:
        return None, details

    target_has_smell = None
    plan_ok = None

    if status is not None:
        if "target_has_smell" in status:
            target_has_smell = bool(status.get("target_has_smell"))
        if "plan_ok" in status:
            plan_ok = bool(status.get("plan_ok"))

    if target_has_smell is False:
        return "target_has_no_smell", details

    if plan_ok is False:
        return "planner_plan_not_ok", details

    return "planner_contract_not_ok", details


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        required=True,
        help="Path to orchestrator/config.yml",
    )
    args = parser.parse_args()

    project_root = Path.cwd().resolve()
    orchestrator_config_path = Path(args.config).resolve()
    orchestrator_cfg = load_yaml(orchestrator_config_path)

    smell = str(require(orchestrator_cfg, "target.smell"))
    target_name = str(require(orchestrator_cfg, "target.target_name"))
    runs = int(require(orchestrator_cfg, "runs"))

    runs_dir = Path(require(orchestrator_cfg, "output.runs_dir")).resolve()
    instance_dir = runs_dir / instance_dir_name(smell, target_name)
    instance_dir.mkdir(parents=True, exist_ok=True)

    write_yaml(instance_dir / "config.yml", orchestrator_cfg)

    planner_base_config_path = Path(
        require(orchestrator_cfg, "planner.base_config")
    ).resolve()

    source_base_config_path = Path(
        require(orchestrator_cfg, "source_refactor.base_config")
    ).resolve()

    planner_base_cfg = load_yaml(planner_base_config_path)
    source_base_cfg = load_yaml(source_base_config_path)

    print(f"Instance dir: {instance_dir}")
    print(f"Target: {target_name}")
    print(f"Smell: {smell}")
    print(f"Runs requested: {runs}")

    for i in range(1, runs + 1):
        run_id = f"run_{i:03d}"
        run_dir = instance_dir / run_id
        run_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n=== {run_id} / {runs} ===")

        planner_cfg = set_common_mvp_config(
            base_cfg=planner_base_cfg,
            orchestrator_cfg=orchestrator_cfg,
            instance_dir=instance_dir,
            run_id=run_id,
        )

        planner_cfg_path = run_dir / "planner.config.yml"
        write_yaml(planner_cfg_path, planner_cfg)

        planner_cmd = [
            sys.executable,
            "-m",
            "mvp.planner.run",
            "--config",
            str(planner_cfg_path),
        ]

        planner_result = run_command(planner_cmd, cwd=project_root)

        write_text(run_dir / "planner.stdout.txt", planner_result.stdout)
        write_text(run_dir / "planner.stderr.txt", planner_result.stderr)

        if planner_result.returncode != 0:
            print(f"Planner failed with return code {planner_result.returncode}")

            write_stop_file(
                instance_dir=instance_dir,
                reason="planner_process_failed",
                run_id=run_id,
                details={
                    "return_code": planner_result.returncode,
                    "planner_config": str(planner_cfg_path),
                    "stdout_path": str(run_dir / "planner.stdout.txt"),
                    "stderr_path": str(run_dir / "planner.stderr.txt"),
                },
            )

            break

        contract_path = instance_dir / run_id / "planner" / "contract.json"
        status_path = instance_dir / run_id / "planner" / "status.json"

        stop_reason, stop_details = detect_planner_stop_reason(
            contract_path=contract_path,
            status_path=status_path,
        )

        if stop_reason is not None:
            print(f"Stopping after Planner: {stop_reason}")

            write_stop_file(
                instance_dir=instance_dir,
                reason=stop_reason,
                run_id=run_id,
                details=stop_details,
            )

            break

        print(f"Planner contract: {contract_path}")

        source_cfg_base = set_common_mvp_config(
            base_cfg=source_base_cfg,
            orchestrator_cfg=orchestrator_cfg,
            instance_dir=instance_dir,
            run_id=run_id,
        )

        source_cfg = set_planner_contract_path(
            source_cfg_base,
            contract_path=contract_path,
        )

        source_cfg_path = run_dir / "source_refactor.config.yml"
        write_yaml(source_cfg_path, source_cfg)

        source_cmd = [
            sys.executable,
            "-m",
            "mvp.source_refactor.run",
            "--config",
            str(source_cfg_path),
        ]

        source_result = run_command(source_cmd, cwd=project_root)

        write_text(run_dir / "source_refactor.stdout.txt", source_result.stdout)
        write_text(run_dir / "source_refactor.stderr.txt", source_result.stderr)

        if source_result.returncode != 0:
            print(f"SourceRefactor failed with return code {source_result.returncode}")
        else:
            print("SourceRefactor finished")

    print(f"\nDone: {instance_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())