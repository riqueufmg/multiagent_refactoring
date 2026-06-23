from __future__ import annotations

import re
from pathlib import Path


def tail_text(text: str, max_lines: int = 180) -> str:
    lines = text.splitlines()
    return "\n".join(lines[-max_lines:])


def normalize_repo_rel_path(path: str) -> str:
    return path.strip().replace("\\", "/")


def extract_java_files_from_build_log(
    build_log: str,
    repo_path: str | Path,
) -> list[str]:
    """
    Extract Java files mentioned in Maven/Javac/Surefire logs.

    This does not classify the error type. It only collects files that appear
    in the build log so the repair node can provide them as editable context.
    """
    repo = Path(repo_path).resolve()
    repo_str = str(repo).replace("\\", "/")

    found: set[str] = set()

    abs_pattern = re.compile(r"(/[^:\s]+?\.java)(?::|\[|\s|$)")
    for match in abs_pattern.finditer(build_log):
        abs_file = Path(match.group(1)).resolve()

        try:
            rel = abs_file.relative_to(repo)
        except ValueError:
            continue

        found.add(normalize_repo_rel_path(str(rel)))

    rel_pattern = re.compile(
        r"\b((?:src/main|src/test)/java/[^:\s]+?\.java)(?::|\[|\s|$)"
    )
    for match in rel_pattern.finditer(build_log):
        found.add(normalize_repo_rel_path(match.group(1)))

    for line in build_log.splitlines():
        normalized = line.replace("\\", "/")

        if repo_str not in normalized or ".java" not in normalized:
            continue

        start = normalized.find(repo_str)
        end = normalized.find(".java", start)

        if start < 0 or end < 0:
            continue

        abs_candidate = normalized[start:end + len(".java")]
        abs_file = Path(abs_candidate).resolve()

        try:
            rel = abs_file.relative_to(repo)
        except ValueError:
            continue

        found.add(normalize_repo_rel_path(str(rel)))

    return sorted(found)


def build_repair_allowed_files(
    original_allowed_files: list[str],
    applied_files: list[str],
    files_mentioned_by_build_log: list[str],
) -> list[str]:
    """
    Repair can edit:
    - files originally allowed for the block;
    - files already changed by the executor;
    - Java files explicitly mentioned by the build log.
    """
    return sorted(
        {
            normalize_repo_rel_path(str(p))
            for p in (
                list(original_allowed_files)
                + list(applied_files)
                + list(files_mentioned_by_build_log)
            )
            if str(p).strip()
        }
    )