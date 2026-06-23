from typing import Any, TypedDict

class SourceRefactorState(TypedDict, total=False):
    config_path: str
    config: dict[str, Any]

    run_id: str
    run_dir: str
    source_refactor_dir: str

    # plan data
    planner_contract_path: str
    planner_contract: dict[str, Any]
    planner_dir: str
    planner_plan_path: str
    planner_input_path: str
    planner_input: dict[str, Any]

    input_plan: dict[str, Any]
    executable_plan: dict[str, Any]

    repo_path: str
    project_name: str

    # target data
    smell: str
    smell_name: str
    target_type: str
    target_name: str
    target_source_root: str
    target_file: str
    target_files: list[str]

    # plan blocks data
    current_block_index: int
    current_block: dict[str, Any]

    status: dict[str, Any]
    contract: dict[str, Any]
    stop_reason: str

    # data
    initial_commit: str
    last_good_commit: str
    final_commit: str

    workspace_clean: bool
    block_commits: list[dict[str, str]]
    repair_commits: list[dict[str, str]]
    block_summaries: list[dict[str, Any]]

    current_block_dir: str
    current_block_id: str
    current_block_commit: str

    allowed_files: list[str]
    files_context: list[dict[str, str]]

    files_to_write: list
    files_to_delete: list

    # executor data
    executor_system_prompt_path: str
    execute_plan_prompt_path: str
    executor_system_prompt: str
    execute_plan_prompt: str
    execute_plan_rendered: str
    execute_plan_raw: str
    execute_plan_result: dict[str, Any]

    executor_existing_files: list[str]
    executor_new_files: list[str]
    executor_files: list[str]
    executor_rejected_files: list[str]

    applied_files: list[str]

    # compilation data
    compile_return_code: int
    compile_ok: bool
    compile_log_path: str
    compile_log: str

    # repair data
    repair_compile_attempt: int
    repair_compile_ok: bool
    repair_compile_error: str
    repair_compile_result: dict[str, Any]
    repair_compile_files: list[str]
    repair_allowed_files: list[str]

    # retry data
    block_attempt: int
    max_block_attempts: int

    executor_ok: bool
    executor_error: str
    executor_feedback: str

    apply_ok: bool
    apply_error: str

    rollback_reason: str
    rolled_back: bool
    rollback_to: str

    # open rewrite
    openrewrite_ok: bool
    openrewrite_return_code: int
    openrewrite_log_path: str
    openrewrite_recipe_path: str
    openrewrite_command: list[str]