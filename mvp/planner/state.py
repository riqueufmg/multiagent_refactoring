from typing import Any, TypedDict


class PlannerState(TypedDict, total=False):
    config_path: str
    config: dict[str, Any]

    project_name: str
    project_root: str
    repo_path: str

    run_id: str
    run_dir: str
    planner_dir: str

    smell: str
    smell_name: str
    target_type: str
    target_name: str

    target_file: str
    target_code: str
    target_class_fqn: str
    target_source_root: str
    target_files: list[str]

    designite_dir: str
    designite_smells_csv: str
    target_has_smell: bool

    planner_system_prompt_path: str
    planner_smell_prompt_path: str
    planner_system_prompt: str
    planner_smell_prompt: str
    planner_rendered_prompt: str

    planner_input: dict[str, Any]
    planner_input_json: str
    planner_raw: str
    plan: dict[str, Any]

    plan_ok: bool
    plan_error: str
    stop_reason: str

    status: dict[str, Any]
    contract: dict[str, Any]