from __future__ import annotations

from pathlib import Path
from typing import Any

from mvp.source_refactor.lib.json_utils import write_json

def read_text_file(path: str | Path) -> str:
    p = Path(path).resolve()

    with p.open("r", encoding="utf-8") as f:
        return f.read()


def write_text_file(path: str | Path, content: str) -> None:
    p = Path(path).resolve()
    p.parent.mkdir(parents=True, exist_ok=True)

    with p.open("w", encoding="utf-8") as f:
        f.write(content)


def delete_file(path: str | Path) -> None:
    p = Path(path).resolve()

    if p.exists() and p.is_file():
        p.unlink()


def ensure_path_inside_repo(repo_path: str | Path, relative_path: str) -> Path:
    repo = Path(repo_path).resolve()
    target = (repo / relative_path).resolve()

    try:
        target.relative_to(repo)
    except ValueError:
        raise ValueError(f"Path escapes repository: {relative_path}")

    return target


def load_files_context(repo_path: str | Path, files: list[str]) -> list[dict[str, str]]:
    context: list[dict[str, str]] = []

    for file_path in files:
        abs_path = ensure_path_inside_repo(repo_path, file_path)

        if not abs_path.exists():
            context.append(
                {
                    "path": file_path,
                    "exists": "false",
                    "content": "",
                }
            )
            continue

        if not abs_path.is_file():
            raise ValueError(f"Expected file but found directory: {file_path}")

        context.append(
            {
                "path": file_path,
                "exists": "true",
                "content": read_text_file(abs_path),
            }
        )

    return context

def apply_llm_file_changes(
    *,
    repo_path: str | Path,
    result: dict[str, Any],
    allowed_files: set[str],
    artifact_dir: str | Path,
    artifact_prefix: str,
) -> tuple[bool, list[str], str]:
    """
    Apply files_to_write/files_to_delete returned by an LLM.

    Expected result format:
    {
      "files_to_write": [
        {"path": "...", "content": "..."}
      ],
      "files_to_delete": [],
      "notes": "..."
    }
    """
    repo = Path(repo_path).resolve()
    out_dir = Path(artifact_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    applied_files: list[str] = []

    try:
        files_to_write = result.get("files_to_write", [])
        files_to_delete = result.get("files_to_delete", [])

        if not isinstance(files_to_write, list):
            raise ValueError("files_to_write must be a list")

        if not isinstance(files_to_delete, list):
            raise ValueError("files_to_delete must be a list")

        normalized_allowed = {
            str(path).strip().replace("\\", "/")
            for path in allowed_files
        }

        for item in files_to_write:
            if not isinstance(item, dict):
                raise ValueError("Each files_to_write item must be an object")

            rel_path = str(item.get("path", "")).strip().replace("\\", "/")

            if rel_path not in normalized_allowed:
                raise ValueError(f"Attempted to write file outside allowed_files: {rel_path}")

            content = item.get("content")

            if not isinstance(content, str):
                raise ValueError(f"Missing or invalid content for file: {rel_path}")

            abs_path = ensure_path_inside_repo(repo, rel_path)
            write_text_file(abs_path, content)
            applied_files.append(rel_path)

        for raw_path in files_to_delete:
            rel_path = str(raw_path).strip().replace("\\", "/")

            if rel_path not in normalized_allowed:
                raise ValueError(f"Attempted to delete file outside allowed_files: {rel_path}")

            abs_path = ensure_path_inside_repo(repo, rel_path)
            delete_file(abs_path)
            applied_files.append(rel_path)

        write_json(
            out_dir / f"{artifact_prefix}.applied.json",
            {
                "ok": True,
                "applied_files": applied_files,
            },
        )

        return True, applied_files, ""

    except Exception as exc:
        error = str(exc)

        write_json(
            out_dir / f"{artifact_prefix}.apply_error.json",
            {
                "ok": False,
                "error": error,
                "applied_files": applied_files,
            },
        )

        return False, applied_files, error