from __future__ import annotations

import subprocess
from pathlib import Path


def run_command(
    command: list[str],
    cwd: str | Path,
    timeout: int,
) -> tuple[int, str]:
    try:
        completed = subprocess.run(
            command,
            cwd=str(cwd),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout,
        )

        return completed.returncode, completed.stdout or ""

    except subprocess.TimeoutExpired as exc:
        output = exc.stdout or ""

        if isinstance(output, bytes):
            output = output.decode("utf-8", errors="replace")

        return 124, output + "\n[TIMEOUT]\n"