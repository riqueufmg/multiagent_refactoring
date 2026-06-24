from __future__ import annotations

from pathlib import Path

from mvp.quality_checker.lib.subprocess_utils import run_command


def git_current_commit(repo_path: str | Path) -> str:
    code, output = run_command(
        ["git", "rev-parse", "HEAD"],
        cwd=repo_path,
        timeout=60,
    )

    if code != 0:
        raise RuntimeError(f"Failed to get current commit:\n{output}")

    return output.strip()


def git_status_porcelain(repo_path: str | Path) -> str:
    code, output = run_command(
        ["git", "status", "--porcelain"],
        cwd=repo_path,
        timeout=60,
    )

    if code != 0:
        raise RuntimeError(f"Failed to get git status:\n{output}")

    return output


def git_reset_hard(repo_path: str | Path, commit: str) -> str:
    code, output = run_command(
        ["git", "reset", "--hard", commit],
        cwd=repo_path,
        timeout=120,
    )

    if code != 0:
        raise RuntimeError(f"Failed to reset repository to {commit}:\n{output}")

    return output


def git_clean_workspace(repo_path: str | Path) -> str:
    code, output = run_command(
        ["git", "clean", "-fd"],
        cwd=repo_path,
        timeout=120,
    )

    if code != 0:
        raise RuntimeError(f"Failed to clean repository:\n{output}")

    return output


def git_commit_exists(repo_path: str | Path, commit: str) -> bool:
    code, _ = run_command(
        ["git", "cat-file", "-e", f"{commit}^{{commit}}"],
        cwd=repo_path,
        timeout=60,
    )

    return code == 0