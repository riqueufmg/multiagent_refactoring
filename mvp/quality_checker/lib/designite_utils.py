from __future__ import annotations

from pathlib import Path
from typing import Any

from mvp.quality_checker.lib.subprocess_utils import run_command


def run_designite(
    *,
    designite_jar: str | Path,
    repo_path: str | Path,
    output_dir: str | Path,
    timeout: int,
) -> dict[str, Any]:
    jar = Path(designite_jar).expanduser().resolve()
    repo = Path(repo_path).expanduser().resolve()
    out = Path(output_dir).expanduser().resolve()

    out.mkdir(parents=True, exist_ok=True)

    command = [
        "java",
        "-jar",
        str(jar),
        "-i",
        str(repo),
        "-o",
        str(out),
    ]

    return_code, output = run_command(
        command,
        cwd=repo,
        timeout=timeout,
    )

    log_path = out / "designite.log"
    command_path = out / "designite.command.txt"

    log_path.write_text(output, encoding="utf-8", errors="replace")
    command_path.write_text(" ".join(command) + "\n", encoding="utf-8")

    csv_files = sorted(str(p) for p in out.rglob("*.csv"))

    return {
        "ok": return_code == 0,
        "return_code": return_code,
        "command": command,
        "output_dir": str(out),
        "log_path": str(log_path),
        "csv_files": csv_files,
    }