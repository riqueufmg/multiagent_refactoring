import json
import subprocess

from pathlib import Path
from typing import Any

from mvp.source_refactor.lib.subprocess_utils import run_command

def git_current_commit(repo_path: str | Path) -> str:
    code, out = run_command(
        ["git", "rev-parse", "HEAD"],
        cwd=repo_path,
    )

    if code != 0:
        raise RuntimeError(f"Could not get current git commit:\n{out}")

    return out.strip()

def git_status_porcelain(repo_path: str | Path) -> str:
    code, out = run_command(
        ["git", "status", "--porcelain"],
        cwd=repo_path,
    )

    if code != 0:
        raise RuntimeError(f"Could not get git status:\n{out}")

    return out.strip()

def ensure_clean_git_workspace(repo_path: str | Path) -> None:
    status = git_status_porcelain(repo_path)

    if status:
        raise RuntimeError(
            "Repository has uncommitted changes. "
            "Please commit, stash, or reset before running source_refactor.\n\n"
            f"Git status:\n{status}"
        )

def git_commit_all(repo_path: str | Path, message: str) -> str:
    code, out = run_command(
        ["git", "add", "-A"],
        cwd=repo_path,
    )

    if code != 0:
        raise RuntimeError(f"Could not git add files:\n{out}")

    status = git_status_porcelain(repo_path)

    if not status:
        return git_current_commit(repo_path)

    code, out = run_command(
        ["git", "commit", "-m", message],
        cwd=repo_path,
    )

    if code != 0:
        raise RuntimeError(f"Could not create git commit:\n{out}")

    return git_current_commit(repo_path)

def git_clean_workspace(repo_path: str | Path) -> None:
    code, out = run_command(
        ["git", "clean", "-fd"],
        cwd=repo_path,
    )

    if code != 0:
        raise RuntimeError(f"Could not clean repository:\n{out}")

def git_reset_hard(repo_path: str | Path, commit: str) -> str:
    code, out = run_command(
        ["git", "reset", "--hard", commit],
        cwd=repo_path,
    )

    if code != 0:
        raise RuntimeError(f"Could not reset repository to {commit}:\n{out}")

    return out

def _run_git_for_artifact(
    repo_path: str | Path,
    args: list[str],
    timeout: int = 120,
) -> tuple[int, str]:
    completed = subprocess.run(
        ["git", *args],
        cwd=str(repo_path),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
    )
    return completed.returncode, completed.stdout

def _parse_name_status(name_status_text: str) -> list[dict[str, Any]]:
    changed_files: list[dict[str, Any]] = []

    for line in name_status_text.splitlines():
        line = line.strip()
        if not line:
            continue

        parts = line.split("\t")
        status = parts[0]

        if status.startswith("R") and len(parts) >= 3:
            changed_files.append(
                {
                    "status": "R",
                    "score": status[1:],
                    "old_path": parts[1],
                    "path": parts[2],
                }
            )
            continue

        if status.startswith("C") and len(parts) >= 3:
            changed_files.append(
                {
                    "status": "C",
                    "score": status[1:],
                    "old_path": parts[1],
                    "path": parts[2],
                }
            )
            continue

        if len(parts) >= 2:
            changed_files.append(
                {
                    "status": status,
                    "path": parts[1],
                }
            )

    return changed_files

def write_commit_diff_artifacts(
    repo_path: str | Path,
    commit: str,
    output_dir: str | Path,
    timeout: int = 120,
) -> dict[str, Any]:
    """
    Writes diff artifacts for a committed block.

    Files created:
    - block.diff
    - block.diffstat.txt
    - block.name_status.txt
    - block.changed_files.json
    """
    repo = Path(repo_path)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    diff_path = out / "block.diff"
    diffstat_path = out / "block.diffstat.txt"
    name_status_path = out / "block.name_status.txt"
    changed_files_path = out / "block.changed_files.json"

    diff_rc, diff_text = _run_git_for_artifact(
        repo,
        [
            "show",
            "--find-renames",
            "--find-copies",
            "--format=medium",
            commit,
        ],
        timeout=timeout,
    )
    diff_path.write_text(diff_text, encoding="utf-8", errors="replace")

    diffstat_rc, diffstat_text = _run_git_for_artifact(
        repo,
        [
            "show",
            "--find-renames",
            "--find-copies",
            "--stat",
            commit,
        ],
        timeout=timeout,
    )
    diffstat_path.write_text(diffstat_text, encoding="utf-8", errors="replace")

    name_status_rc, name_status_text = _run_git_for_artifact(
        repo,
        [
            "show",
            "--name-status",
            "--format=",
            commit,
        ],
        timeout=timeout,
    )
    name_status_path.write_text(name_status_text, encoding="utf-8", errors="replace")

    changed_files = _parse_name_status(name_status_text)

    production_files = [
        item["path"]
        for item in changed_files
        if str(item.get("path", "")).startswith("src/main/")
    ]

    test_files = [
        item["path"]
        for item in changed_files
        if str(item.get("path", "")).startswith("src/test/")
    ]

    payload: dict[str, Any] = {
        "commit": commit,
        "ok": diff_rc == 0 and diffstat_rc == 0 and name_status_rc == 0,
        "return_codes": {
            "diff": diff_rc,
            "diffstat": diffstat_rc,
            "name_status": name_status_rc,
        },
        "paths": {
            "diff": str(diff_path),
            "diffstat": str(diffstat_path),
            "name_status": str(name_status_path),
            "changed_files": str(changed_files_path),
        },
        "changed_files": changed_files,
        "production_files": production_files,
        "test_files": test_files,
        "changed_files_count": len(changed_files),
        "production_files_count": len(production_files),
        "test_files_count": len(test_files),
    }

    changed_files_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    return payload