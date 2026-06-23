from pathlib import Path

from mvp.source_refactor.lib.subprocess_utils import run_command


def run_compile_command(
    repo_path: str | Path,
    command: list[str],
    timeout: int | None = None,
) -> tuple[int, str]:
    if not command:
        raise ValueError("Compile command cannot be empty")

    return run_command(
        command,
        cwd=repo_path,
        timeout=timeout,
    )