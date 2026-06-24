from __future__ import annotations

from langgraph.graph import END, StateGraph

from mvp.quality_checker.state import QualityCheckerState
from mvp.quality_checker.nodes import (
    load_config_node,
    init_run_node,
    load_source_refactor_contract_node,
    resolve_commits_node,
    run_designite_before_node,
    run_designite_after_node,
    run_refactoringminer_node,
    analyze_designite_results_node,
    save_status_node,
)


def build_quality_checker_graph():
    g = StateGraph(QualityCheckerState)

    g.add_node("load_config", load_config_node)
    g.add_node("init_run", init_run_node)
    g.add_node("load_source_refactor_contract", load_source_refactor_contract_node)
    g.add_node("resolve_commits", resolve_commits_node)
    g.add_node("run_designite_before", run_designite_before_node)
    g.add_node("run_designite_after", run_designite_after_node)
    g.add_node("run_refactoringminer", run_refactoringminer_node)
    g.add_node("analyze_designite_results", analyze_designite_results_node)
    g.add_node("save_status", save_status_node)

    g.set_entry_point("load_config")

    g.add_edge("load_config", "init_run")
    g.add_edge("init_run", "load_source_refactor_contract")
    g.add_edge("load_source_refactor_contract", "resolve_commits")
    g.add_edge("resolve_commits", "run_designite_before")
    g.add_edge("run_designite_before", "run_designite_after")
    g.add_edge("run_designite_after", "run_refactoringminer")
    g.add_edge("run_refactoringminer", "analyze_designite_results")
    g.add_edge("analyze_designite_results", "save_status")
    g.add_edge("save_status", END)

    return g.compile()