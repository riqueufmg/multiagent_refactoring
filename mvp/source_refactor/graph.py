from langgraph.graph import StateGraph, END

from mvp.source_refactor.state import SourceRefactorState
from mvp.source_refactor.nodes import (
    load_config_node,
    init_run_node,
    load_planner_contract_node,
    load_plan_node,
    prepare_executable_plan_node,
    ensure_clean_workspace_node,
    record_initial_commit_node,
    stage_block_node,
    lock_workspace_node,
    resolve_files_context_node,
    openrewrite_node,
    after_resolve_files_context,
    after_openrewrite,
    execute_plan_node,
    after_execute_plan,
    retry_executor_node,
    rollback_final_node,
    after_apply_changes,
    apply_changes_node,
    compile_source_node,
    after_compile_source,
    repair_compile_node,
    after_repair_compile,
    after_compile_after_repair,
    promote_block_node,
    advance_block_node,
    after_advance_block,
    save_status_node,
)

def build_source_refactor_graph():
    g = StateGraph(SourceRefactorState)

    g.add_node("load_config", load_config_node)
    g.add_node("init_run", init_run_node)
    g.add_node("load_planner_contract", load_planner_contract_node)
    g.add_node("load_plan", load_plan_node)
    g.add_node("prepare_executable_plan", prepare_executable_plan_node)
    g.add_node("ensure_clean_workspace", ensure_clean_workspace_node)
    g.add_node("record_initial_commit", record_initial_commit_node)
    g.add_node("stage_block", stage_block_node)
    g.add_node("lock_workspace", lock_workspace_node)
    g.add_node("resolve_files_context", resolve_files_context_node)
    g.add_node("openrewrite", openrewrite_node)
    g.add_node("execute_plan", execute_plan_node)
    g.add_node("retry_executor", retry_executor_node)
    g.add_node("rollback_final", rollback_final_node)
    g.add_node("apply_changes", apply_changes_node)
    g.add_node("compile_source", compile_source_node)
    g.add_node("compile_after_repair", compile_source_node)
    g.add_node("repair_compile", repair_compile_node)
    g.add_node("promote_block", promote_block_node)
    g.add_node("advance_block", advance_block_node)
    g.add_node("save_status", save_status_node)

    g.set_entry_point("load_config")

    g.add_edge("load_config", "init_run")
    g.add_edge("init_run", "load_planner_contract")
    g.add_edge("load_planner_contract", "load_plan")
    g.add_edge("load_plan", "prepare_executable_plan")
    g.add_edge("prepare_executable_plan", "ensure_clean_workspace")
    g.add_edge("ensure_clean_workspace", "record_initial_commit")
    g.add_edge("record_initial_commit", "stage_block")
    g.add_edge("stage_block", "lock_workspace")
    g.add_edge("lock_workspace", "resolve_files_context")
    g.add_conditional_edges(
        "resolve_files_context",
        after_resolve_files_context,
        {
            "openrewrite": "openrewrite",
            "execute_plan": "execute_plan",
        },
    )
    g.add_conditional_edges(
        "openrewrite",
        after_openrewrite,
        {
            "execute_plan": "execute_plan",
            "rollback_final": "rollback_final",
        },
    )
    g.add_conditional_edges(
        "execute_plan",
        after_execute_plan,
        {
            "apply_changes": "apply_changes",
            "retry_executor": "retry_executor",
            "rollback_final": "rollback_final",
        },
    )
    g.add_conditional_edges(
        "apply_changes",
        after_apply_changes,
        {
            "compile_source": "compile_source",
            "retry_executor": "retry_executor",
            "rollback_final": "rollback_final",
        },
    )
    g.add_edge("retry_executor", "lock_workspace")
    g.add_conditional_edges(
        "compile_source",
        after_compile_source,
        {
            "promote_block": "promote_block",
            "repair_compile": "repair_compile",
            "rollback_final": "rollback_final",
        },
    )
    g.add_conditional_edges(
        "repair_compile",
        after_repair_compile,
        {
            "compile_after_repair": "compile_after_repair",
            "rollback_final": "rollback_final",
        },
    )
    g.add_conditional_edges(
        "compile_after_repair",
        after_compile_after_repair,
        {
            "promote_block": "promote_block",
            "rollback_final": "rollback_final",
        },
    )
    g.add_edge("rollback_final", "save_status")
    g.add_edge("promote_block", "advance_block")
    g.add_conditional_edges(
        "advance_block",
        after_advance_block,
        {
            "stage_block": "stage_block",
            "save_status": "save_status",
        },
    )
    g.add_edge("save_status", END)

    return g.compile()