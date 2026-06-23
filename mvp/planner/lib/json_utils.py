import json
from pathlib import Path

def _extract_json_object_only(s: str) -> str:
    s = (s or "").strip()
    if not s:
        return s

    if s.startswith("{") and s.endswith("}"):
        return s

    i = s.find("{")
    j = s.rfind("}")
    if i != -1 and j != -1 and j > i:
        return s[i : j + 1].strip()

    return s

def _load_meta_or_init(meta_path: Path, repo_path: Path, base_commit: str | None) -> dict:
    if meta_path.exists():
        try:
            return json.loads(meta_path.read_text(encoding="utf-8"))
        except Exception:
            pass

    return {"repo_path": str(repo_path), "base_commit": base_commit}