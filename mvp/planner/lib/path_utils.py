import re
from pathlib import Path

def _is_safe_repo_rel_path(p: str) -> bool:
    if not p or "\x00" in p:
        return False

    pp = Path(p)
    if pp.is_absolute():
        return False

    if ":" in p.split("/")[0]:
        return False

    parts = pp.as_posix().split("/")
    if any(part == ".." for part in parts):
        return False

    return True

def _validate_allowed_paths(rel_paths: list[str], allowed: set[str]) -> tuple[bool, str]:
    for rp in rel_paths:
        if not _is_safe_repo_rel_path(rp):
            return False, f"unsafe path: {rp}"
        if rp not in allowed:
            return False, f"path not in allowed_paths: {rp}"
    return True, ""

def _infer_source_root_from_target(repo_path: Path, target_rel: str, target_fqn: str) -> str:
    pkg_parts = target_fqn.split(".")[:-1]
    pkg_path = "/".join(pkg_parts)

    tr = Path(target_rel).as_posix()

    suffix = f"{pkg_path}/{target_fqn.split('.')[-1]}.java"
    if tr.endswith(suffix):
        src_root = tr[: -len(suffix)].rstrip("/")
        if src_root:
            return src_root

    p = Path(tr)
    up = len(pkg_parts) + 1
    for _ in range(up):
        p = p.parent

    return p.as_posix()

def _java_fqn_to_path(repo_path: Path, class_fqn: str, source_root_rel: str) -> str:
    rel = Path(source_root_rel) / Path(class_fqn.replace(".", "/") + ".java")
    return str((repo_path / rel).resolve())

def _extract_fqn_from_java(code: str, filename: str) -> str:
    m = re.search(r'^\s*package\s+([a-zA-Z0-9_.]+)\s*;', code, re.MULTILINE)
    pkg = m.group(1) if m else ""
    cls = Path(filename).stem
    return f"{pkg}.{cls}" if pkg else cls

def _to_repo_rel(repo_path: Path, p: str) -> str:
    pp = Path(p)
    if pp.is_absolute():
        try:
            return str(pp.resolve().relative_to(repo_path))
        except Exception:
            return str(pp.as_posix()).lstrip("/")
    return pp.as_posix()

def _read_target_file(repo_path: Path, target_file: str) -> tuple[str, str]:
    if not target_file or "\x00" in target_file:
        raise RuntimeError("target_file is empty/invalid")

    tf = Path(target_file)

    if tf.is_absolute():
        abs_p = tf.resolve()
    else:
        abs_p = (repo_path / tf).resolve()

    if repo_path != abs_p and repo_path not in abs_p.parents:
        raise RuntimeError(f"target_file is outside repo: {abs_p}")

    rel = str(abs_p.relative_to(repo_path)).replace("\\", "/")

    if not abs_p.exists() or not abs_p.is_file():
        raise RuntimeError(f"target_file does not exist or is not a file: {rel}")

    code = abs_p.read_text(encoding="utf-8", errors="replace")
    return rel, code

def _infer_target_type_from_name(target_name: str) -> str:
    name = (target_name or "").strip()
    if not name:
        raise ValueError("target_name is empty")

    last = name.split(".")[-1]
    if last[:1].isupper():
        return "class"

    return "package"

def java_file_to_fqn(rel_path: str, source_root: str) -> str:
    path = Path(rel_path).with_suffix("")
    root = Path(source_root)

    try:
        rel = path.relative_to(root)
    except ValueError as exc:
        raise ValueError(
            "Java file path is not under source_root: "
            f"rel_path={rel_path}, source_root={source_root}"
        ) from exc

    return ".".join(rel.parts)

def java_files_to_fqns(rel_paths: list[str], source_root: str) -> set[str]:
    return {
        java_file_to_fqn(path, source_root)
        for path in rel_paths
        if path.endswith(".java") and not path.endswith("package-info.java")
    }

def fqn_to_java_path(fqn: str, source_root: str) -> str:
    return str(Path(source_root) / Path(*fqn.split("."))) + ".java"