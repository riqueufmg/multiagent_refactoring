import re

from pathlib import Path

from mvp.planner.lib.path_utils import (
    _to_repo_rel,
    java_file_to_fqn,
)

## check metions for the class name in a content
def _contains_word(content: str, word: str) -> bool:
    return re.search(rf"\b{re.escape(word)}\b", content) is not None

## parser java files in test path to find test for a specific list of source classes
def find_related_tests_for_classes(
    repo_path: str,
    production_files: list[str],
    source_root: str,
) -> list[str]:
    repo = Path(repo_path).resolve()

    class_fqns: set[str] = set()
    class_names: set[str] = set()

    ## get each fqn of source classes
    for prod_file in production_files:
        
        ## check only .java extensions
        if not prod_file.endswith(".java"):
            continue

        ## add name of elegible classes
        class_names.add(Path(prod_file).stem)

        try:
            ## add fqn of elegible classes
            class_fqns.add(java_file_to_fqn(prod_file, source_root))
        except ValueError:
            continue

    ## check if exists classes to be evaluated
    if not class_fqns and not class_names:
        return []

    related_tests: set[str] = set()

    ## get all .java files from the repository
    for test_file in repo.rglob("*.java"):
        
        ## get repo path of java files
        rel_path = _to_repo_rel(repo, str(test_file))

        normalized = rel_path.replace("\\", "/")

        ## check for src/test in the path
        if "src/test" not in normalized:
            continue

        try:
            ## save test candidate content in a variable
            content = test_file.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue

        ## check if the content contains any of the class fqns
        if any(fqn in content for fqn in class_fqns):
            related_tests.add(normalized)
            continue

        ## check if the content contains any of the class names
        if any(_contains_word(content, name) for name in class_names):
            related_tests.add(normalized)
            continue

    ## return a list of tests based on the source codes list.
    return sorted(related_tests)