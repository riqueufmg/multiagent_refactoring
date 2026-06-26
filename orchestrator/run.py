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


def set_source_refactor_contract_path(
    quality_checker_cfg: dict[str, Any],
    contract_path: Path,
) -> dict[str, Any]:
    cfg = deepcopy(quality_checker_cfg)
    contract = str(contract_path)

    # Main expected locations.
    cfg.setdefault("input", {})
    cfg["input"]["source_refactor_contract"] = contract
    cfg["input"]["source_refactor_contract_path"] = contract

    # Extra aliases. They are harmless if ignored by the MVP.
    cfg["source_refactor_contract"] = contract
    cfg["source_refactor_contract_path"] = contract

    cfg.setdefault("source_refactor", {})
    cfg["source_refactor"]["contract"] = contract
    cfg["source_refactor"]["contract_path"] = contract

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

def get_optional(data: dict[str, Any] | None, dotted_key: str, default: Any = None) -> Any:
    if not isinstance(data, dict):
        return default

    current: Any = data

    for part in dotted_key.split("."):
        if not isinstance(current, dict) or part not in current:
            return default
        current = current[part]

    return current


def json_exists(path: Path) -> bool:
    return path.exists() and path.is_file()


def build_run_summary(run_dir: Path) -> dict[str, Any]:
    run_id = run_dir.name

    planner_contract_path = run_dir / "planner" / "contract.json"
    planner_status_path = run_dir / "planner" / "status.json"

    source_contract_path = run_dir / "source_refactor" / "contract.json"
    source_status_path = run_dir / "source_refactor" / "status.json"

    checker_contract_path = run_dir / "quality_checker" / "contract.json"
    checker_status_path = run_dir / "quality_checker" / "status.json"
    checker_skipped_path = run_dir / "quality_checker.skipped.json"

    planner_contract = read_json_if_exists(planner_contract_path)
    planner_status = read_json_if_exists(planner_status_path)

    source_contract = read_json_if_exists(source_contract_path)
    source_status = read_json_if_exists(source_status_path)

    checker_contract = read_json_if_exists(checker_contract_path)
    checker_status = read_json_if_exists(checker_status_path)
    checker_skipped = read_json_if_exists(checker_skipped_path)

    source_execution = get_optional(source_contract, "execution", {}) or {}
    source_commits = get_optional(source_contract, "commits", {}) or {}

    checker_smells = get_optional(checker_status, "smells", {}) or {}
    checker_metrics = get_optional(checker_status, "metrics", {}) or {}
    checker_refactoringminer = get_optional(checker_status, "refactoringminer", {}) or {}

    return {
        "run_id": run_id,
        "paths": {
            "run_dir": str(run_dir),
            "planner_config": str(run_dir / "planner.config.yml"),
            "source_refactor_config": str(run_dir / "source_refactor.config.yml"),
            "quality_checker_config": str(run_dir / "quality_checker.config.yml"),
            "planner_stdout": str(run_dir / "planner.stdout.txt"),
            "planner_stderr": str(run_dir / "planner.stderr.txt"),
            "source_refactor_stdout": str(run_dir / "source_refactor.stdout.txt"),
            "source_refactor_stderr": str(run_dir / "source_refactor.stderr.txt"),
            "quality_checker_stdout": str(run_dir / "quality_checker.stdout.txt"),
            "quality_checker_stderr": str(run_dir / "quality_checker.stderr.txt"),
        },
        "planner": {
            "contract_exists": json_exists(planner_contract_path),
            "status_exists": json_exists(planner_status_path),
            "ok": get_optional(planner_contract, "ok", None),
            "target_has_smell": get_optional(planner_status, "target_has_smell", None),
            "plan_ok": get_optional(planner_status, "plan_ok", None),
            "contract_path": str(planner_contract_path) if planner_contract_path.exists() else "",
            "status_path": str(planner_status_path) if planner_status_path.exists() else "",
        },
        "source_refactor": {
            "contract_exists": json_exists(source_contract_path),
            "status_exists": json_exists(source_status_path),
            "ok": get_optional(source_contract, "ok", None),
            "contract_path": str(source_contract_path) if source_contract_path.exists() else "",
            "status_path": str(source_status_path) if source_status_path.exists() else "",
            "execution": {
                "blocks_count": source_execution.get("blocks_count", None),
                "blocks_applied": source_execution.get("blocks_applied", None),
                "blocks_failed": source_execution.get("blocks_failed", None),
                "failed_block_id": source_execution.get("failed_block_id", ""),
                "failed_stage": source_execution.get("failed_stage", ""),
                "rolled_back": source_execution.get("rolled_back", None),
                "rollback_reason": source_execution.get("rollback_reason", ""),
                "stop_reason": source_execution.get("stop_reason", ""),
            },
            "commits": {
                "initial_commit": source_commits.get("initial_commit", ""),
                "last_good_commit": source_commits.get("last_good_commit", ""),
                "final_commit": source_commits.get("final_commit", ""),
            },
        },
        "quality_checker": {
            "contract_exists": json_exists(checker_contract_path),
            "status_exists": json_exists(checker_status_path),
            "skipped": checker_skipped is not None,
            "skip_reason": get_optional(checker_skipped, "reason", ""),
            "ok": get_optional(checker_status, "ok", None),
            "contract_path": str(checker_contract_path) if checker_contract_path.exists() else "",
            "status_path": str(checker_status_path) if checker_status_path.exists() else "",
            "designite": {
                "before_ok": get_optional(checker_status, "designite.before_ok", None),
                "after_ok": get_optional(checker_status, "designite.after_ok", None),
                "before_dir": get_optional(checker_status, "designite.before_dir", ""),
                "after_dir": get_optional(checker_status, "designite.after_dir", ""),
            },
            "smells": {
                "before_count": checker_smells.get("before_count", None),
                "after_count": checker_smells.get("after_count", None),
                "removed_count": checker_smells.get("removed_count", None),
                "added_count": checker_smells.get("added_count", None),
                "persisted_count": checker_smells.get("persisted_count", None),
                "removed": checker_smells.get("removed", []),
                "added": checker_smells.get("added", []),
            },
            "metrics": {
                "target": checker_metrics.get("target", ""),
                "values": checker_metrics.get("values", {}),
            },
            "refactoringminer": {
                "enabled": checker_refactoringminer.get("enabled", None),
                "ok": checker_refactoringminer.get("ok", None),
                "refactorings_count": checker_refactoringminer.get(
                    "refactorings_count",
                    None,
                ),
                "types": checker_refactoringminer.get("types", {}),
                "json_path": checker_refactoringminer.get("json_path", ""),
            },
        },
    }


def build_instance_summary(
    *,
    instance_dir: Path,
    orchestrator_cfg: dict[str, Any],
    runs_requested: int,
) -> dict[str, Any]:
    run_dirs = sorted(
        p for p in instance_dir.iterdir()
        if p.is_dir() and re.fullmatch(r"run_\d{3}", p.name)
    )

    runs_summary = [build_run_summary(run_dir) for run_dir in run_dirs]

    planner_contracts = [
        r for r in runs_summary
        if r["planner"]["contract_exists"]
    ]
    source_contracts = [
        r for r in runs_summary
        if r["source_refactor"]["contract_exists"]
    ]
    checker_statuses = [
        r for r in runs_summary
        if r["quality_checker"]["status_exists"]
    ]

    stop = read_json_if_exists(instance_dir / "stop.json")

    return {
        "summary_version": "1.0",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "instance_dir": str(instance_dir),
        "config_path": str(instance_dir / "config.yml"),
        "target": {
            "project": get_optional(orchestrator_cfg, "project.name", ""),
            "repo_path": get_optional(orchestrator_cfg, "project.repo_path", ""),
            "smell": get_optional(orchestrator_cfg, "target.smell", ""),
            "smell_name": get_optional(orchestrator_cfg, "target.smell_name", ""),
            "target_type": get_optional(orchestrator_cfg, "target.target_type", ""),
            "target_name": get_optional(orchestrator_cfg, "target.target_name", ""),
        },
        "runs_requested": runs_requested,
        "runs_found": len(runs_summary),
        "stop": stop or {},
        "counts": {
            "planner_contracts": len(planner_contracts),
            "planner_ok": sum(
                1 for r in runs_summary
                if r["planner"]["ok"] is True
            ),
            "source_refactor_contracts": len(source_contracts),
            "source_refactor_ok": sum(
                1 for r in runs_summary
                if r["source_refactor"]["ok"] is True
            ),
            "quality_checker_statuses": len(checker_statuses),
            "quality_checker_ok": sum(
                1 for r in runs_summary
                if r["quality_checker"]["ok"] is True
            ),
            "quality_checker_skipped": sum(
                1 for r in runs_summary
                if r["quality_checker"]["skipped"] is True
            ),
            "smells_removed_total": sum(
                int(r["quality_checker"]["smells"]["removed_count"] or 0)
                for r in runs_summary
            ),
            "smells_added_total": sum(
                int(r["quality_checker"]["smells"]["added_count"] or 0)
                for r in runs_summary
            ),
            "refactorings_total": sum(
                int(
                    r["quality_checker"]["refactoringminer"][
                        "refactorings_count"
                    ] or 0
                )
                for r in runs_summary
            ),
        },
        "runs": runs_summary,
    }


def write_instance_summary(
    *,
    instance_dir: Path,
    orchestrator_cfg: dict[str, Any],
    runs_requested: int,
) -> Path:
    summary = build_instance_summary(
        instance_dir=instance_dir,
        orchestrator_cfg=orchestrator_cfg,
        runs_requested=runs_requested,
    )

    summary_path = instance_dir / "summary.json"
    write_json(summary_path, summary)

    return summary_path

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

    write_instance_summary(
        instance_dir=instance_dir,
        orchestrator_cfg=orchestrator_cfg,
        runs_requested=runs,
    )

    planner_base_config_path = Path(
        require(orchestrator_cfg, "planner.base_config")
    ).resolve()

    source_base_config_path = Path(
        require(orchestrator_cfg, "source_refactor.base_config")
    ).resolve()

    quality_checker_base_config_path = Path(
        require(orchestrator_cfg, "quality_checker.base_config")
    ).resolve()

    planner_base_cfg = load_yaml(planner_base_config_path)
    source_base_cfg = load_yaml(source_base_config_path)
    quality_checker_base_cfg = load_yaml(quality_checker_base_config_path)

    print(f"Instance dir: {instance_dir}")
    print(f"Target: {target_name}")
    print(f"Smell: {smell}")
    print(f"Runs requested: {runs}")

    for i in range(1, runs + 1):
        run_id = f"run_{i:03d}"
        run_dir = instance_dir / run_id
        run_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n=== {run_id} / {runs} ===")

        # Planner
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

            write_instance_summary(
                instance_dir=instance_dir,
                orchestrator_cfg=orchestrator_cfg,
                runs_requested=runs,
            )

            break

        planner_contract_path = instance_dir / run_id / "planner" / "contract.json"
        planner_status_path = instance_dir / run_id / "planner" / "status.json"

        stop_reason, stop_details = detect_planner_stop_reason(
            contract_path=planner_contract_path,
            status_path=planner_status_path,
        )

        if stop_reason is not None:
            print(f"Stopping after Planner: {stop_reason}")

            write_stop_file(
                instance_dir=instance_dir,
                reason=stop_reason,
                run_id=run_id,
                details=stop_details,
            )

            write_instance_summary(
                instance_dir=instance_dir,
                orchestrator_cfg=orchestrator_cfg,
                runs_requested=runs,
            )

            break

        print(f"Planner contract: {planner_contract_path}")

        # SourceRefactor
        source_cfg_base = set_common_mvp_config(
            base_cfg=source_base_cfg,
            orchestrator_cfg=orchestrator_cfg,
            instance_dir=instance_dir,
            run_id=run_id,
        )

        source_cfg = set_planner_contract_path(
            source_cfg_base,
            contract_path=planner_contract_path,
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

        source_refactor_contract_path = (
            instance_dir / run_id / "source_refactor" / "contract.json"
        )

        # QualityChecker
        if not source_refactor_contract_path.exists():
            print("QualityChecker skipped: missing source_refactor contract")

            write_json(
                run_dir / "quality_checker.skipped.json",
                {
                    "skipped": True,
                    "reason": "missing_source_refactor_contract",
                    "source_refactor_contract": str(source_refactor_contract_path),
                    "source_refactor_return_code": source_result.returncode,
                },
            )

            write_instance_summary(
                instance_dir=instance_dir,
                orchestrator_cfg=orchestrator_cfg,
                runs_requested=runs,
            )

            continue

        quality_checker_cfg_base = set_common_mvp_config(
            base_cfg=quality_checker_base_cfg,
            orchestrator_cfg=orchestrator_cfg,
            instance_dir=instance_dir,
            run_id=run_id,
        )

        quality_checker_cfg = set_source_refactor_contract_path(
            quality_checker_cfg_base,
            contract_path=source_refactor_contract_path,
        )

        quality_checker_cfg_path = run_dir / "quality_checker.config.yml"
        write_yaml(quality_checker_cfg_path, quality_checker_cfg)

        quality_checker_cmd = [
            sys.executable,
            "-m",
            "mvp.quality_checker.run",
            "--config",
            str(quality_checker_cfg_path),
        ]

        quality_checker_result = run_command(
            quality_checker_cmd,
            cwd=project_root,
        )

        write_text(
            run_dir / "quality_checker.stdout.txt",
            quality_checker_result.stdout,
        )
        write_text(
            run_dir / "quality_checker.stderr.txt",
            quality_checker_result.stderr,
        )

        if quality_checker_result.returncode != 0:
            print(
                "QualityChecker failed with return code "
                f"{quality_checker_result.returncode}"
            )
        else:
            print("QualityChecker finished")
        
        summary_path = write_instance_summary(
            instance_dir=instance_dir,
            orchestrator_cfg=orchestrator_cfg,
            runs_requested=runs,
        )

        print(f"Summary updated: {summary_path}")

    summary_path = write_instance_summary(
        instance_dir=instance_dir,
        orchestrator_cfg=orchestrator_cfg,
        runs_requested=runs,
    )

    print(f"\nSummary: {summary_path}")

    print(f"\nDone: {instance_dir}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())