import subprocess
from pathlib import Path

def _run(cmd: list[str], cwd: Path, env: dict | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        cwd=str(cwd),
        env=env,
        capture_output=True,
        text=True,
    )

def _tail(s: str, n: int = 40) -> str:
    lines = (s or "").splitlines()
    return "\n".join(lines[-n:]).strip()