from mvp.planner.lib.path_utils import (
    java_file_to_fqn,
    fqn_to_java_path,
)
from mvp.planner.lib.test_utils import find_related_tests_for_classes

def enrich_plan_with_visibility_ops(plan: dict, context: dict) -> dict:
    internal_deps = context.get("internal_deps") or []
    target_files = context.get("target_files") or []
    target_source_root = context.get("target_source_root") or ""

    class_to_file: dict[str, str] = {}

    for file_path in target_files:
        fqn = java_file_to_fqn(file_path, target_source_root)
        class_to_file[fqn] = file_path

    related_by_class: dict[str, set[str]] = {}

    for src, dst in internal_deps:
        related_by_class.setdefault(src, set()).add(dst)
        related_by_class.setdefault(dst, set()).add(src)

    original_blocks = plan.get("blocks") or []
    enriched_blocks = []
    next_id = 1

    for block in original_blocks:
        ops = block.get("ops") or []

        move_ops = [
            op for op in ops
            if str(op.get("op", "")).strip() == "MOVE_CLASS"
        ]

        if not move_ops:
            block["id"] = next_id
            enriched_blocks.append(block)
            next_id += 1
            continue

        moved_old_fqns: list[str] = []
        moved_new_fqns: list[str] = []

        for op in move_ops:
            inputs = op.get("inputs") or []
            outputs = op.get("outputs") or []

            if not inputs or not outputs:
                continue

            moved_old_fqns.append(str(inputs[0]).strip())
            moved_new_fqns.append(str(outputs[0]).strip())

        moved_old_set = set(moved_old_fqns)
        moved_new_set = set(moved_new_fqns)

        if not moved_old_fqns:
            block["id"] = next_id
            enriched_blocks.append(block)
            next_id += 1
            continue

        related_remaining_classes: set[str] = set()

        for old_fqn in moved_old_fqns:
            for related in related_by_class.get(old_fqn, set()):
                if related in class_to_file and related not in moved_old_set:
                    related_remaining_classes.add(related)

        new_ops = [
            op for op in ops
            if str(op.get("op", "")).strip() in {"CREATE_PACKAGE", "MOVE_CLASS"}
        ]

        visibility_inputs = sorted(moved_new_set | related_remaining_classes)

        new_ops.append(
            {
                "op": "UPDATE_VISIBILITY",
                "inputs": visibility_inputs,
                "outputs": [],
                "details": (
                    "After moving the whole cluster to the destination package, "
                    "update only the minimum required visibility in moved classes "
                    "and related remaining classes so the project can compile. "
                    "Do not change behavior. Do not move additional classes."
                ),
                "risk": "medium",
                "api_change": True,
            }
        )

        new_files = set(block.get("files") or [])

        for old_fqn in moved_old_fqns:
            if old_fqn in class_to_file:
                new_files.add(class_to_file[old_fqn])

        for new_fqn in moved_new_fqns:
            new_files.add(fqn_to_java_path(new_fqn, target_source_root))

        for related in related_remaining_classes:
            if related in class_to_file:
                new_files.add(class_to_file[related])

        block["id"] = next_id
        block["goal"] = block.get("goal") or (
            "Move cohesive cluster: " + ", ".join(moved_old_fqns)
        )
        block["files"] = sorted(new_files)
        block["ops"] = new_ops

        enriched_blocks.append(block)
        next_id += 1

    plan["blocks"] = enriched_blocks
    return plan

## enrich plan with related tests for source code files
def enrich_plan_with_related_tests(plan: dict, context: dict) -> dict:
    
    repo_path = context.get("repo_path", "")
    source_root = context.get("target_source_root", "")

    if not repo_path or not source_root:
        return plan

    blocks = plan.get("blocks") or []

    ## the tests will checked block by block
    ## tests refactoring occurs only in the mentioned classes in the block
    for block in blocks:
        files = block.get("files") or []

        production_files = [
            str(file)
            for file in files
            if str(file).startswith("src/main/")
            and str(file).endswith(".java")
        ]

        ## check existing classes in block's plan
        if not production_files:
            continue

        ## get tests from classes out of block's plan
        related_tests = find_related_tests_for_classes(
            repo_path=repo_path,
            production_files=production_files,
            source_root=source_root,
        )

        if not related_tests:
            block["test_files"] = []
            continue

        merged_files = sorted(set(files) | set(related_tests))

        block["files"] = merged_files
        block["test_files"] = related_tests

        ops = block.get("ops") or []

        has_update_tests = any(
            isinstance(op, dict)
            and str(op.get("op", "")).strip() == "UPDATE_TESTS"
            for op in ops
        )

        ## add new block operation to update tests
        if not has_update_tests:
            ops.append(
                {
                    "op": "UPDATE_TESTS",
                    "inputs": related_tests,
                    "outputs": [],
                    "details": (
                        "Update related tests affected by this refactoring block "
                        "so the configured build command passes. Adjust imports, "
                        "package references, moved class references, constructors, "
                        "and assertions only when required. Do not change production "
                        "behavior through tests."
                    ),
                    "risk": "medium",
                    "api_change": False,
                }
            )

        block["ops"] = ops

    plan["blocks"] = blocks
    return plan