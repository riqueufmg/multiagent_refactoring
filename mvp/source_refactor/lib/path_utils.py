from pathlib import Path

def require_absolute_path(value: str, field_name: str) -> Path:
    path = Path(value).expanduser()

    if not path.is_absolute():
        raise ValueError(f"{field_name} must be an absolute path: {value}")

    return path.resolve()

def ensure_file_exists(path: Path, field_name: str) -> Path:
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"{field_name} not found or not a file: {path}")

    return path

def ensure_dir_exists(path: Path, field_name: str) -> Path:
    if not path.exists() or not path.is_dir():
        raise FileNotFoundError(f"{field_name} not found or not a directory: {path}")

    return path

def as_posix_relative(path: Path, base: Path) -> str:
    return str(path.resolve().relative_to(base.resolve())).replace("\\", "/")