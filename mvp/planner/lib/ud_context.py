# mvp/planner/lib/ud_context.py

import csv
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

from mvp.planner.lib.fqn import Fqn
from mvp.planner.lib.java_context import extract_observed_external_calls


LESS_STABLE_RE = re.compile(
    r"following less stable component\(s\):\s*(?P<packages>.+)$",
    re.IGNORECASE,
)


def get_package_name(fqn: str) -> str:
    parts = fqn.split(".")

    if parts and parts[-1][:1].isupper():
        return ".".join(parts[:-1])

    return fqn


def is_test_class(fqn: str) -> bool:
    simple_name = fqn.rsplit(".", 1)[-1]
    return (
        simple_name.endswith("Test")
        or simple_name.endswith("IT")
        or ".test." in fqn.lower()
        or ".tests." in fqn.lower()
    )


def parse_unstable_packages_from_architecture_smells(
    csv_path: str | Path,
    target_package: str,
    smell_name: str = "Unstable Dependency",
) -> list[str]:
    csv_path = Path(csv_path)

    if not csv_path.exists():
        raise FileNotFoundError(f"Architecture smells CSV not found: {csv_path}")

    with csv_path.open(newline="", encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f)

        for row in reader:
            package = (row.get("Package") or "").strip()
            smell = (row.get("Smell") or "").strip()
            description = (row.get("Description") or "").strip()

            if package != target_package or smell != smell_name:
                continue

            match = LESS_STABLE_RE.search(description)

            if not match:
                return []

            raw_packages = match.group("packages").strip().rstrip(".")
            return [
                pkg.strip()
                for pkg in raw_packages.split(";")
                if pkg.strip()
            ]

    return []


def read_graphml_edges(graphml_path: str | Path) -> list[tuple[str, str]]:
    graphml_path = Path(graphml_path)

    if not graphml_path.exists():
        raise FileNotFoundError(f"Dependency graph not found: {graphml_path}")

    ns = {"g": "http://graphml.graphdrawing.org/xmlns"}

    tree = ET.parse(graphml_path)
    root = tree.getroot()

    edges: list[tuple[str, str]] = []

    for edge in root.findall(".//g:edge", ns):
        source = edge.get("source")
        target = edge.get("target")

        if not source or not target:
            continue

        if is_test_class(source) or is_test_class(target):
            continue

        edges.append((source, target))

    return edges


def get_outgoing_dependencies_to_unstable_packages(
    graphml_path: str | Path,
    target_package: str,
    unstable_packages: list[str],
) -> list[dict[str, Any]]:
    unstable_set = set(unstable_packages)
    dependencies: list[dict[str, Any]] = []

    for source, target in read_graphml_edges(graphml_path):
        source_package = get_package_name(source)
        target_package_name = get_package_name(target)

        if source_package != target_package:
            continue

        if target_package_name not in unstable_set:
            continue

        dependencies.append(
            {
                "source": source,
                "target": target,
                "source_package": source_package,
                "target_package": target_package_name,
                "external_calls": [],
            }
        )

    return dependencies


def read_java_code_for_fqn(repo_path: str | Path, class_fqn: str) -> str:
    repo_path = Path(repo_path).resolve()
    path = Fqn(class_fqn).find_in_repo(repo_path)

    if path is None or not path.is_file():
        return ""

    return path.read_text(encoding="utf-8", errors="ignore")


def infer_external_calls_to_target_class(
    repo_path: str | Path,
    source_class_fqn: str,
    target_class_fqn: str,
) -> list[str]:
    source_code = read_java_code_for_fqn(repo_path, source_class_fqn)

    if not source_code:
        return []

    observed_calls = extract_observed_external_calls(source_code)

    target_simple_name = target_class_fqn.rsplit(".", 1)[-1]

    methods = observed_calls.get(target_simple_name, [])

    return [
        f"{target_simple_name}.{method}()"
        for method in methods
    ]


def enrich_dependencies_with_external_calls(
    repo_path: str | Path,
    dependencies: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    enriched: list[dict[str, Any]] = []

    for dep in dependencies:
        dep = dict(dep)

        dep["external_calls"] = infer_external_calls_to_target_class(
            repo_path=repo_path,
            source_class_fqn=dep["source"],
            target_class_fqn=dep["target"],
        )

        enriched.append(dep)

    return enriched


def build_ud_planner_input(
    repo_path: str | Path,
    architecture_smells_csv: str | Path,
    dependency_graphml: str | Path,
    target_package: str,
) -> dict[str, Any]:
    unstable_packages = parse_unstable_packages_from_architecture_smells(
        csv_path=architecture_smells_csv,
        target_package=target_package,
    )

    outgoing_dependencies = get_outgoing_dependencies_to_unstable_packages(
        graphml_path=dependency_graphml,
        target_package=target_package,
        unstable_packages=unstable_packages,
    )

    outgoing_dependencies = enrich_dependencies_with_external_calls(
        repo_path=repo_path,
        dependencies=outgoing_dependencies,
    )

    return {
        "target": target_package,
        "unstable_packages": unstable_packages,
        "outgoing_dependencies": [
            {
                "source": dep["source"],
                "target": dep["target"],
                "external_calls": dep["external_calls"],
            }
            for dep in outgoing_dependencies
        ],
    }