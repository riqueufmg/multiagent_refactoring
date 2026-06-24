from __future__ import annotations

from typing import Any, TypedDict

class QualityCheckerState(TypedDict, total=False):
    # Input
    config_path: str
    config: dict[str, Any]
    source_refactor_contract_path: str
    source_refactor_contract: dict[str, Any]

    # Run metadata
    run_id: str
    run_dir: str
    quality_checker_dir: str

    # Project
    project_name: str
    repo_path: str

    # Target
    smell: str
    smell_name: str
    target_type: str
    target_name: str

    # SourceRefactor summary
    source_refactor_ok: bool
    blocks_count: int
    blocks_applied: int
    blocks_failed: int
    failed_block_id: str
    failed_stage: str
    rolled_back: bool
    rollback_reason: str
    stop_reason: str

    # Commits
    initial_commit: str
    last_good_commit: str
    final_commit: str
    before_commit: str
    after_commit: str

    # Designite
    designite_before_dir: str
    designite_after_dir: str
    designite_before_ok: bool
    designite_after_ok: bool
    designite_before_log_path: str
    designite_after_log_path: str

    # RefactoringMiner
    refactoringminer_enabled: bool
    refactoringminer_ok: bool
    refactoringminer_json_path: str
    refactoringminer_log_path: str
    refactorings_count: int
    refactoring_types: dict[str, int]

    # Analysis
    smells_before: list[dict[str, Any]]
    smells_after: list[dict[str, Any]]
    smells_removed: list[dict[str, Any]]
    smells_added: list[dict[str, Any]]
    smells_persisted: list[dict[str, Any]]

    target_metrics: dict[str, list[Any]]

    # Output
    status: dict[str, Any]
    contract: dict[str, Any]