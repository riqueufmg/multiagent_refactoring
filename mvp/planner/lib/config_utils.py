from pathlib import Path
from typing import Any
import yaml

def load_config(config_path: str | Path) -> dict[str, Any]:
    path = Path(config_path).resolve()

    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with path.open("r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}

    if not isinstance(cfg, dict):
        raise ValueError(f"Config must be a YAML object: {path}")

    return cfg


def require_config_value(cfg: dict[str, Any], dotted_key: str) -> Any:
    current: Any = cfg

    for part in dotted_key.split("."):
        if not isinstance(current, dict) or part not in current:
            raise ValueError(f"Missing required config value: {dotted_key}")
        current = current[part]

    return current