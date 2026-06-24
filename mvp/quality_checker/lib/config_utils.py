from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def load_config(path: str | Path) -> dict[str, Any]:
    config_path = Path(path).expanduser().resolve()

    with config_path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict):
        raise ValueError(f"Invalid YAML config: {config_path}")

    return data


def get_config_value(
    cfg: dict[str, Any],
    dotted_key: str,
    default: Any = None,
) -> Any:
    current: Any = cfg

    for part in dotted_key.split("."):
        if not isinstance(current, dict) or part not in current:
            return default

        current = current[part]

    return current


def require_config_value(
    cfg: dict[str, Any],
    dotted_key: str,
) -> Any:
    value = get_config_value(cfg, dotted_key, None)

    if value is None:
        raise ValueError(f"Missing required config value: {dotted_key}")

    return value