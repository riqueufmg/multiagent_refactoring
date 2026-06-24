from __future__ import annotations

import shutil
from pathlib import Path

from mvp.quality_checker.state import QualityCheckerState

from mvp.quality_checker.lib.config_utils import (
    get_config_value,
    load_config,
    require_config_value,
)
from mvp.quality_checker.lib.json_utils import read_json, write_json
from mvp.quality_checker.lib.path_utils import (
    ensure_dir_exists,
    ensure_file_exists,
    require_absolute_path,
)
from mvp.quality_checker.lib.git_utils import (
    git_commit_exists,
    git_current_commit,
    git_reset_hard,
    git_status_porcelain,
)
from mvp.quality_checker.lib.designite_utils import run_designite
from mvp.quality_checker.lib.refactoringminer_utils import run_refactoringminer
from mvp.quality_checker.lib.analysis_utils import (
    compare_smells,
    compare_target_metrics,
    load_designite_smells,
    load_target_metrics,
)


def load_config_node(state: QualityCheckerState) -> QualityCheckerState:
    config_path = require_absolute_path(state["config_path"], "config_path")
    ensure_file_exists(config_path, "config_path")

    cfg = load_config(config_path)

    source_refactor_contract_path = require_absolute_path(
        str(require_config_value(cfg, "input.source_refactor_contract")),
        "input.source_refactor_contract",
    )
    ensure_file_exists(
        source_refactor_contract_path,
        "input.source_refactor_contract",
    )

    runs_dir = require_absolute_path(
        str(require_config_value(cfg, "output.runs_dir")),
        "output.runs_dir",
    )
    runs_dir.mkdir(parents=True, exist_ok=True)

    state["config_path"] = str(config_path)
    state["config"] = cfg
    state["source_refactor_contract_path"] = str(source_refactor_contract_path)

    return state


def init_run_node(state: QualityCheckerState) -> QualityCheckerState:
    cfg = state["config"]

    source_refactor_contract_path = Path(
        state["source_refactor_contract_path"]
    ).resolve()

    runs_dir = require_absolute_path(
        str(require_config_value(cfg, "output.runs_dir")),
        "output.runs_dir",
    )

    run_id_cfg = cfg.get("mvp", {}).get("run_id", "auto")

    if source_refactor_contract_path.parent.name == "source_refactor":
        inferred_run_dir = source_refactor_contract_path.parent.parent
        inferred_run_id = inferred_run_dir.name
    else:
        inferred_run_dir = runs_dir / "quality_checker_manual"
        inferred_run_id = "quality_checker_manual"

    if run_id_cfg and run_id_cfg != "auto":
        run_id = str(run_id_cfg)
        run_dir = runs_dir / run_id
    else:
        run_id = inferred_run_id
        run_dir = inferred_run_dir

    quality_checker_dir = run_dir / "quality_checker"
    quality_checker_dir.mkdir(parents=True, exist_ok=True)

    state["run_id"] = run_id
    state["run_dir"] = str(run_dir)
    state["quality_checker_dir"] = str(quality_checker_dir)

    shutil.copyfile(
        state["config_path"],
        quality_checker_dir / "config.snapshot.yml",
    )

    return state


def load_source_refactor_contract_node(
    state: QualityCheckerState,
) -> QualityCheckerState:
    quality_checker_dir = Path(state["quality_checker_dir"])
    contract_path = Path(state["source_refactor_contract_path"]).resolve()

    contract = read_json(contract_path)

    if contract.get("producer") != "source_refactor":
        raise ValueError("Input contract was not produced by source_refactor")

    project = contract.get("project", {}) or {}
    target = contract.get("target", {}) or {}
    execution = contract.get("execution", {}) or {}
    commits = contract.get("commits", {}) or {}

    repo_path = require_absolute_path(
        str(project.get("repo_path", "")),
        "source_refactor.project.repo_path",
    )
    ensure_dir_exists(repo_path, "source_refactor.project.repo_path")

    state["source_refactor_contract"] = contract

    state["repo_path"] = str(repo_path)
    state["project_name"] = str(project.get("name", ""))

    state["smell"] = str(target.get("smell", ""))
    state["smell_name"] = str(target.get("smell_name", ""))
    state["target_type"] = str(target.get("target_type", ""))
    state["target_name"] = str(target.get("target_name", ""))

    state["source_refactor_ok"] = bool(contract.get("ok", False))
    state["blocks_count"] = int(execution.get("blocks_count", 0) or 0)
    state["blocks_applied"] = int(execution.get("blocks_applied", 0) or 0)
    state["blocks_failed"] = int(execution.get("blocks_failed", 0) or 0)
    state["failed_block_id"] = str(execution.get("failed_block_id", ""))
    state["failed_stage"] = str(execution.get("failed_stage", ""))
    state["rolled_back"] = bool(execution.get("rolled_back", False))
    state["rollback_reason"] = str(execution.get("rollback_reason", ""))
    state["stop_reason"] = str(execution.get("stop_reason", ""))

    state["initial_commit"] = str(commits.get("initial_commit", ""))
    state["last_good_commit"] = str(commits.get("last_good_commit", ""))
    state["final_commit"] = str(commits.get("final_commit", ""))

    shutil.copyfile(
        contract_path,
        quality_checker_dir / "input_contract.json",
    )

    return state


def resolve_commits_node(state: QualityCheckerState) -> QualityCheckerState:
    repo_path = Path(state["repo_path"]).resolve()

    before_commit = str(state.get("initial_commit", "")).strip()
    after_commit = str(state.get("last_good_commit", "")).strip()

    if not after_commit:
        after_commit = str(state.get("final_commit", "")).strip()

    if not before_commit:
        raise ValueError("Missing initial_commit in source_refactor contract")

    if not after_commit:
        raise ValueError("Missing last_good_commit/final_commit in source_refactor contract")

    if not git_commit_exists(repo_path, before_commit):
        raise ValueError(f"initial_commit does not exist in repo: {before_commit}")

    if not git_commit_exists(repo_path, after_commit):
        raise ValueError(f"after commit does not exist in repo: {after_commit}")

    quality_checker_dir = Path(state["quality_checker_dir"])
    git_dir = quality_checker_dir / "git"
    git_dir.mkdir(parents=True, exist_ok=True)

    entry_commit = git_current_commit(repo_path)
    entry_status = git_status_porcelain(repo_path)

    state["before_commit"] = before_commit
    state["after_commit"] = after_commit

    write_json(
        git_dir / "commits.json",
        {
            "entry_commit": entry_commit,
            "entry_status": entry_status,
            "before_commit": before_commit,
            "after_commit": after_commit,
            "policy": {
                "before": "initial_commit",
                "after": "last_good_commit_or_final_commit_fallback",
                "restore_repo_after_check": False,
            },
        },
    )

    return state


def run_designite_before_node(state: QualityCheckerState) -> QualityCheckerState:
    cfg = state["config"]

    repo_path = Path(state["repo_path"]).resolve()
    quality_checker_dir = Path(state["quality_checker_dir"])

    designite_jar = require_absolute_path(
        str(require_config_value(cfg, "tools.designite_jar")),
        "tools.designite_jar",
    )
    ensure_file_exists(designite_jar, "tools.designite_jar")

    timeout = int(get_config_value(cfg, "designite.timeout", 600))

    before_commit = state["before_commit"]

    git_reset_hard(repo_path, before_commit)

    before_dir = quality_checker_dir / "designite" / "before"

    result = run_designite(
        designite_jar=designite_jar,
        repo_path=repo_path,
        output_dir=before_dir,
        timeout=timeout,
    )

    write_json(before_dir / "designite.status.json", result)

    state["designite_before_dir"] = str(before_dir)
    state["designite_before_ok"] = bool(result.get("ok", False))
    state["designite_before_log_path"] = str(result.get("log_path", ""))

    return state


def run_designite_after_node(state: QualityCheckerState) -> QualityCheckerState:
    cfg = state["config"]

    repo_path = Path(state["repo_path"]).resolve()
    quality_checker_dir = Path(state["quality_checker_dir"])

    designite_jar = require_absolute_path(
        str(require_config_value(cfg, "tools.designite_jar")),
        "tools.designite_jar",
    )
    ensure_file_exists(designite_jar, "tools.designite_jar")

    timeout = int(get_config_value(cfg, "designite.timeout", 600))

    after_commit = state["after_commit"]

    git_reset_hard(repo_path, after_commit)

    after_dir = quality_checker_dir / "designite" / "after"

    result = run_designite(
        designite_jar=designite_jar,
        repo_path=repo_path,
        output_dir=after_dir,
        timeout=timeout,
    )

    write_json(after_dir / "designite.status.json", result)

    state["designite_after_dir"] = str(after_dir)
    state["designite_after_ok"] = bool(result.get("ok", False))
    state["designite_after_log_path"] = str(result.get("log_path", ""))

    return state


def run_refactoringminer_node(state: QualityCheckerState) -> QualityCheckerState:
    cfg = state["config"]

    enabled = bool(get_config_value(cfg, "refactoringminer.enabled", True))
    state["refactoringminer_enabled"] = enabled

    quality_checker_dir = Path(state["quality_checker_dir"])
    out_dir = quality_checker_dir / "refactoringminer"
    out_dir.mkdir(parents=True, exist_ok=True)

    if not enabled:
        state["refactoringminer_ok"] = True
        state["refactorings_count"] = 0
        state["refactoring_types"] = {}
        state["refactoringminer_json_path"] = ""
        state["refactoringminer_log_path"] = ""

        write_json(
            out_dir / "summary.json",
            {
                "ok": True,
                "enabled": False,
                "refactorings_count": 0,
                "types": {},
            },
        )

        return state

    refactoringminer_bin = require_absolute_path(
        str(require_config_value(cfg, "tools.refactoringminer_bin")),
        "tools.refactoringminer_bin",
    )
    ensure_file_exists(refactoringminer_bin, "tools.refactoringminer_bin")

    timeout = int(get_config_value(cfg, "refactoringminer.timeout", 600))

    result = run_refactoringminer(
        refactoringminer_bin=refactoringminer_bin,
        repo_path=state["repo_path"],
        before_commit=state["before_commit"],
        after_commit=state["after_commit"],
        output_dir=out_dir,
        timeout=timeout,
    )

    state["refactoringminer_ok"] = bool(result.get("ok", False))
    state["refactorings_count"] = int(result.get("refactorings_count", 0) or 0)
    state["refactoring_types"] = result.get("types", {}) or {}
    state["refactoringminer_json_path"] = str(result.get("json_path", ""))
    state["refactoringminer_log_path"] = str(result.get("log_path", ""))

    return state


def analyze_designite_results_node(
    state: QualityCheckerState,
) -> QualityCheckerState:
    before_dir = state["designite_before_dir"]
    after_dir = state["designite_after_dir"]

    smells_before = load_designite_smells(before_dir)
    smells_after = load_designite_smells(after_dir)

    smell_diff = compare_smells(smells_before, smells_after)

    before_metrics = load_target_metrics(
        before_dir,
        target_name=state["target_name"],
        target_type=state["target_type"],
    )
    after_metrics = load_target_metrics(
        after_dir,
        target_name=state["target_name"],
        target_type=state["target_type"],
    )

    target_metrics = compare_target_metrics(before_metrics, after_metrics)

    state["smells_before"] = smells_before
    state["smells_after"] = smells_after
    state["smells_removed"] = smell_diff["removed"]
    state["smells_added"] = smell_diff["added"]
    state["smells_persisted"] = smell_diff["persisted"]
    state["target_metrics"] = target_metrics

    quality_checker_dir = Path(state["quality_checker_dir"])
    analysis_dir = quality_checker_dir / "analysis"
    analysis_dir.mkdir(parents=True, exist_ok=True)

    write_json(
        analysis_dir / "smells.before.json",
        smells_before,
    )
    write_json(
        analysis_dir / "smells.after.json",
        smells_after,
    )
    write_json(
        analysis_dir / "smells.diff.json",
        {
            "removed": smell_diff["removed"],
            "added": smell_diff["added"],
            "persisted": smell_diff["persisted"],
        },
    )
    write_json(
        analysis_dir / "target_metrics.before.json",
        before_metrics,
    )
    write_json(
        analysis_dir / "target_metrics.after.json",
        after_metrics,
    )
    write_json(
        analysis_dir / "target_metrics.diff.json",
        target_metrics,
    )

    return state


def save_status_node(state: QualityCheckerState) -> QualityCheckerState:
    quality_checker_dir = Path(state["quality_checker_dir"])

    designite_ok = bool(state.get("designite_before_ok", False)) and bool(
        state.get("designite_after_ok", False)
    )

    refactoringminer_ok = bool(state.get("refactoringminer_ok", True))

    final_ok = designite_ok and refactoringminer_ok

    status_path = quality_checker_dir / "status.json"
    contract_path = quality_checker_dir / "contract.json"

    status = {
        "mvp": "quality_checker",
        "ok": final_ok,
        "run_id": state.get("run_id", ""),
        "project": state.get("project_name", ""),
        "repo_path": state.get("repo_path", ""),
        "target": {
            "target_type": state.get("target_type", ""),
            "target_name": state.get("target_name", ""),
            "smell": state.get("smell", ""),
            "smell_name": state.get("smell_name", ""),
        },
        "source_refactor": {
            "ok": state.get("source_refactor_ok", False),
            "blocks_count": state.get("blocks_count", 0),
            "blocks_applied": state.get("blocks_applied", 0),
            "blocks_failed": state.get("blocks_failed", 0),
            "failed_block_id": state.get("failed_block_id", ""),
            "failed_stage": state.get("failed_stage", ""),
            "rolled_back": state.get("rolled_back", False),
            "rollback_reason": state.get("rollback_reason", ""),
            "stop_reason": state.get("stop_reason", ""),
        },
        "commits": {
            "before": state.get("before_commit", ""),
            "after": state.get("after_commit", ""),
            "initial_commit": state.get("initial_commit", ""),
            "last_good_commit": state.get("last_good_commit", ""),
            "final_commit": state.get("final_commit", ""),
        },
        "designite": {
            "before_ok": state.get("designite_before_ok", False),
            "after_ok": state.get("designite_after_ok", False),
            "before_dir": state.get("designite_before_dir", ""),
            "after_dir": state.get("designite_after_dir", ""),
            "before_log": state.get("designite_before_log_path", ""),
            "after_log": state.get("designite_after_log_path", ""),
        },
        "smells": {
            "before_count": len(state.get("smells_before", [])),
            "after_count": len(state.get("smells_after", [])),
            "removed_count": len(state.get("smells_removed", [])),
            "added_count": len(state.get("smells_added", [])),
            "persisted_count": len(state.get("smells_persisted", [])),
            "removed": state.get("smells_removed", []),
            "added": state.get("smells_added", []),
        },
        "metrics": {
            "target": state.get("target_name", ""),
            "values": state.get("target_metrics", {}),
        },
        "refactoringminer": {
            "enabled": state.get("refactoringminer_enabled", False),
            "ok": state.get("refactoringminer_ok", False),
            "json_path": state.get("refactoringminer_json_path", ""),
            "log_path": state.get("refactoringminer_log_path", ""),
            "refactorings_count": state.get("refactorings_count", 0),
            "types": state.get("refactoring_types", {}),
        },
        "artifacts": {
            "quality_checker_dir": str(quality_checker_dir),
            "status": str(status_path),
            "contract": str(contract_path),
            "input_contract": str(quality_checker_dir / "input_contract.json"),
            "analysis_dir": str(quality_checker_dir / "analysis"),
            "designite_before": state.get("designite_before_dir", ""),
            "designite_after": state.get("designite_after_dir", ""),
            "refactoringminer_dir": str(quality_checker_dir / "refactoringminer"),
        },
        "status_path": str(status_path),
        "contract_path": str(contract_path),
    }

    contract = {
        "producer": "quality_checker",
        "version": "1.0",
        "ok": final_ok,
        "run_id": state.get("run_id", ""),
        "input": {
            "source_refactor_contract": state.get(
                "source_refactor_contract_path",
                "",
            ),
        },
        "project": {
            "name": state.get("project_name", ""),
            "repo_path": state.get("repo_path", ""),
        },
        "target": {
            "target_type": state.get("target_type", ""),
            "target_name": state.get("target_name", ""),
            "smell": state.get("smell", ""),
            "smell_name": state.get("smell_name", ""),
        },
        "commits": {
            "before": state.get("before_commit", ""),
            "after": state.get("after_commit", ""),
            "initial_commit": state.get("initial_commit", ""),
            "last_good_commit": state.get("last_good_commit", ""),
            "final_commit": state.get("final_commit", ""),
        },
        "artifacts": {
            "quality_checker_dir": str(quality_checker_dir),
            "status": str(status_path),
            "designite_before": state.get("designite_before_dir", ""),
            "designite_after": state.get("designite_after_dir", ""),
            "smells_diff": str(quality_checker_dir / "analysis" / "smells.diff.json"),
            "target_metrics_diff": str(
                quality_checker_dir / "analysis" / "target_metrics.diff.json"
            ),
            "refactoringminer_json": state.get("refactoringminer_json_path", ""),
            "refactoringminer_summary": str(
                quality_checker_dir / "refactoringminer" / "summary.json"
            ),
        },
    }

    state["status"] = status
    state["contract"] = contract

    write_json(status_path, status)
    write_json(contract_path, contract)

    return state