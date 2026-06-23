import subprocess
from pathlib import Path

def run_command(
    cmd: list[str],
    cwd: str | Path,
    timeout: int | None = None,
) -> tuple[int, str]:
    result = subprocess.run(
        cmd,
        cwd=str(cwd),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
    )

    return result.returncode, result.stdout