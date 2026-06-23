from pathlib import Path
from typing import Any

import yaml


def load_config(config_path: str | Path) -> dict[str, Any]:
    path = Path(config_path).expanduser().resolve()

    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict):
        raise ValueError(f"Invalid YAML config: {path}")

    return data


def get_config_value(config: dict[str, Any], dotted_key: str, default: Any = None) -> Any:
    current: Any = config

    for part in dotted_key.split("."):
        if not isinstance(current, dict) or part not in current:
            return default
        current = current[part]

    return current


def require_config_value(config: dict[str, Any], dotted_key: str) -> Any:
    value = get_config_value(config, dotted_key)

    if value is None:
        raise ValueError(f"Missing required config value: {dotted_key}")

    return value