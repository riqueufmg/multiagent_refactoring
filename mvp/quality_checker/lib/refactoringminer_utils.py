from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from mvp.quality_checker.lib.subprocess_utils import run_command
from mvp.quality_checker.lib.json_utils import write_json


def run_refactoringminer(
    *,
    refactoringminer_bin: str | Path,
    repo_path: str | Path,
    before_commit: str,
    after_commit: str,
    output_dir: str | Path,
    timeout: int,
    java_home: str | Path | None = None,
) -> dict[str, Any]:
    binary = Path(refactoringminer_bin).expanduser().resolve()
    repo = Path(repo_path).expanduser().resolve()
    out = Path(output_dir).expanduser().resolve()

    out.mkdir(parents=True, exist_ok=True)

    json_path = out / "refactorings.json"
    log_path = out / "refactoringminer.log"
    command_path = out / "refactoringminer.command.txt"
    summary_path = out / "summary.json"

    if before_commit == after_commit:
        summary = {
            "ok": True,
            "skipped": True,
            "reason": "before_commit_equals_after_commit",
            "refactorings_count": 0,
            "types": {},
            "json_path": "",
            "log_path": "",
        }

        write_json(summary_path, summary)
        return summary

    base_command = [
        str(binary),
        "-bc",
        str(repo),
        before_commit,
        after_commit,
        "-json",
        str(json_path),
    ]

    effective_java_home = ""
    if java_home:
        java_home_path = Path(java_home).expanduser().resolve()
        effective_java_home = str(java_home_path)

        command = [
            "env",
            f"JAVA_HOME={effective_java_home}",
            f"PATH={java_home_path / 'bin'}:{os.environ.get('PATH', '')}",
            *base_command,
        ]
    else:
        command = base_command

    command_path.write_text(" ".join(command) + "\n", encoding="utf-8")

    return_code, output = run_command(
        command,
        cwd=repo,
        timeout=timeout,
    )

    log_path.write_text(output, encoding="utf-8", errors="replace")

    refactorings = []
    types: dict[str, int] = {}

    if json_path.exists():
        try:
            data = json.loads(json_path.read_text(encoding="utf-8"))

            commits = data.get("commits", [])
            if isinstance(commits, list):
                for commit in commits:
                    if not isinstance(commit, dict):
                        continue

                    items = commit.get("refactorings", [])
                    if not isinstance(items, list):
                        continue

                    for item in items:
                        if not isinstance(item, dict):
                            continue

                        refactorings.append(item)
                        ref_type = str(item.get("type", "UNKNOWN"))
                        types[ref_type] = types.get(ref_type, 0) + 1

        except Exception as exc:
            summary = {
                "ok": False,
                "return_code": return_code,
                "error": f"failed_to_parse_refactoringminer_json: {exc}",
                "java_home": effective_java_home,
                "command": command,
                "json_path": str(json_path),
                "log_path": str(log_path),
                "refactorings_count": 0,
                "types": {},
            }

            write_json(summary_path, summary)
            return summary

    summary = {
        "ok": return_code == 0,
        "return_code": return_code,
        "skipped": False,
        "java_home": effective_java_home,
        "command": command,
        "json_path": str(json_path),
        "log_path": str(log_path),
        "refactorings_count": len(refactorings),
        "types": types,
    }

    write_json(summary_path, summary)

    return summary