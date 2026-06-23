from pathlib import Path

def extract_package_declaration(code: str) -> str:
    for line in code.splitlines():
        line = line.strip()

        if line.startswith("package ") and line.endswith(";"):
            return line.removeprefix("package ").removesuffix(";").strip()

    return ""

def extract_public_type_name(file_path: Path) -> str:
    return file_path.stem

def java_file_to_fqn(file_path: Path) -> str:
    code = file_path.read_text(encoding="utf-8", errors="replace")
    package_name = extract_package_declaration(code)
    class_name = extract_public_type_name(file_path)

    if package_name:
        return f"{package_name}.{class_name}"

    return class_name

def find_java_fqn_in_repo(repo_path: str | Path, fqn: str) -> str | None:
    repo = Path(repo_path).resolve()

    for java_file in repo.rglob("*.java"):
        # Evita pastas que geralmente não interessam
        parts = set(java_file.parts)
        if "target" in parts or ".git" in parts:
            continue

        try:
            current_fqn = java_file_to_fqn(java_file)
        except Exception:
            continue

        if current_fqn == fqn:
            return str(java_file.relative_to(repo)).replace("\\", "/")

    return None

def java_fqn_to_path(
    fqn: str,
    source_root: str,
) -> str:
    fqn = fqn.strip()

    if not fqn:
        raise ValueError("Java FQN cannot be empty")

    if "." not in fqn:
        raise ValueError(f"Invalid Java FQN: {fqn}")

    class_path = fqn.replace(".", "/") + ".java"

    return str(Path(source_root) / class_path).replace("\\", "/")

def resolve_java_fqn_to_path(
    repo_path: str | Path,
    fqn: str,
    source_root: str,
) -> str:
    existing = find_java_fqn_in_repo(repo_path, fqn)

    if existing:
        return existing

    return java_fqn_to_path(fqn, source_root)

def looks_like_java_class_fqn(value: str) -> bool:
    value = value.strip()

    if "." not in value:
        return False

    if value.endswith("/"):
        return False

    simple_name = value.split(".")[-1]

    if not simple_name:
        return False

    return simple_name[0].isupper()


def normalize_repo_relative_path(path: str) -> str:
    return path.strip().replace("\\", "/")