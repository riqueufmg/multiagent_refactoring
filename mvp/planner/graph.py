from langgraph.graph import StateGraph, END

from mvp.planner.state import PlannerState
from mvp.planner.nodes import (
    load_config_node,
    init_run_node,
    resolve_target_node,
    run_designite_node,
    check_smell_node,
    after_check_smell,
    build_planner_context_node,
    call_planner_node,
    validate_plan_node,
    save_status_node,
)


def build_planner_graph():
    g = StateGraph(PlannerState)

    g.add_node("load_config", load_config_node)
    g.add_node("init_run", init_run_node)
    g.add_node("resolve_target", resolve_target_node)
    g.add_node("run_designite", run_designite_node)
    g.add_node("check_smell", check_smell_node)
    g.add_node("build_planner_context", build_planner_context_node)
    g.add_node("call_planner", call_planner_node)
    g.add_node("validate_plan", validate_plan_node)
    g.add_node("save_status", save_status_node)

    g.set_entry_point("load_config")

    g.add_edge("load_config", "init_run")
    g.add_edge("init_run", "resolve_target")
    g.add_edge("resolve_target", "run_designite")
    g.add_edge("run_designite", "check_smell")

    g.add_conditional_edges(
        "check_smell",
        after_check_smell,
        {
            "build_planner_context": "build_planner_context",
            "save_status": "save_status",
        },
    )

    g.add_edge("build_planner_context", "call_planner")
    g.add_edge("call_planner", "validate_plan")
    g.add_edge("validate_plan", "save_status")
    g.add_edge("save_status", END)

    return g.compile()