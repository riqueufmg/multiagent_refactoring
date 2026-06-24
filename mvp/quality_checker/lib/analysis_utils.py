from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


def _norm(value: Any) -> str:
    return str(value or "").strip()


def _norm_key(value: Any) -> str:
    return _norm(value).lower().replace(" ", "").replace("_", "")


def _read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", errors="replace", newline="") as f:
        reader = csv.DictReader(f)
        return [dict(row) for row in reader]


def _csv_files(root: str | Path) -> list[Path]:
    return sorted(Path(root).expanduser().resolve().rglob("*.csv"))


def _get_by_alias(row: dict[str, str], aliases: set[str]) -> str:
    for key, value in row.items():
        if _norm_key(key) in aliases:
            return _norm(value)

    return ""


def _numeric(value: Any) -> int | float | None:
    text = _norm(value)

    if not text:
        return None

    text = text.replace(",", ".")

    try:
        as_float = float(text)
    except ValueError:
        return None

    if as_float.is_integer():
        return int(as_float)

    return as_float


def _infer_entity(row: dict[str, str]) -> str:
    direct_aliases = {
        "fullyqualifiedname",
        "qualifiedname",
        "fqn",
        "entity",
        "element",
        "classname",
        "typename",
        "packagename",
        "package",
    }

    direct = _get_by_alias(row, direct_aliases)
    if direct and "." in direct:
        return direct

    package_name = _get_by_alias(row, {"package", "packagename"})
    type_name = _get_by_alias(row, {"type", "typename", "class", "classname", "name"})

    if package_name and type_name and not type_name.startswith(package_name):
        return f"{package_name}.{type_name}"

    if direct:
        return direct

    method_name = _get_by_alias(row, {"method", "methodname"})
    if method_name:
        return method_name

    return ""


def _infer_smell_name(row: dict[str, str]) -> str:
    aliases = {
        "smell",
        "smellname",
        "codedsmell",
        "codesmell",
        "designsmell",
        "architecturesmell",
        "typeofsmell",
    }

    value = _get_by_alias(row, aliases)
    if value:
        return value

    for key, val in row.items():
        if "smell" in _norm_key(key):
            return _norm(val)

    return ""


def _infer_level_from_filename(path: Path) -> str:
    name = path.name.lower()

    if "architecture" in name:
        return "architecture"

    if "design" in name:
        return "design"

    if "implementation" in name:
        return "implementation"

    if "method" in name:
        return "method"

    if "type" in name or "class" in name:
        return "class"

    return "unknown"


def _smell_key(item: dict[str, Any]) -> str:
    return "|".join(
        [
            _norm(item.get("level")),
            _norm(item.get("smell")),
            _norm(item.get("entity")),
            _norm(item.get("source")),
        ]
    )


def load_designite_smells(designite_dir: str | Path) -> list[dict[str, Any]]:
    smells: list[dict[str, Any]] = []

    for csv_path in _csv_files(designite_dir):
        name = csv_path.name.lower()

        if "smell" not in name:
            continue

        try:
            rows = _read_csv_rows(csv_path)
        except Exception:
            continue

        for row in rows:
            smell_name = _infer_smell_name(row)
            entity = _infer_entity(row)

            if not smell_name and not entity:
                continue

            item = {
                "level": _infer_level_from_filename(csv_path),
                "smell": smell_name,
                "entity": entity,
                "source": csv_path.name,
                "row": row,
            }

            item["key"] = _smell_key(item)
            smells.append(item)

    return sorted(smells, key=lambda x: x["key"])


def compare_smells(
    before: list[dict[str, Any]],
    after: list[dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    before_by_key = {item["key"]: item for item in before}
    after_by_key = {item["key"]: item for item in after}

    before_keys = set(before_by_key)
    after_keys = set(after_by_key)

    removed = [before_by_key[key] for key in sorted(before_keys - after_keys)]
    added = [after_by_key[key] for key in sorted(after_keys - before_keys)]
    persisted = [after_by_key[key] for key in sorted(before_keys & after_keys)]

    return {
        "removed": removed,
        "added": added,
        "persisted": persisted,
    }


def _is_target_row(
    row: dict[str, str],
    target_name: str,
) -> bool:
    target = _norm(target_name)

    if not target:
        return False

    entity = _infer_entity(row)

    if entity == target:
        return True

    if entity and target.endswith("." + entity):
        return True

    if entity and entity.endswith("." + target.split(".")[-1]):
        return True

    direct_values = {_norm(v) for v in row.values() if _norm(v)}

    if target in direct_values:
        return True

    simple = target.split(".")[-1]
    package = ".".join(target.split(".")[:-1])

    has_simple = simple in direct_values
    has_package = package in direct_values

    return has_simple and (not package or has_package)


def _metric_file_priority(path: Path, target_type: str) -> int:
    name = path.name.lower()

    if target_type == "class":
        if "type" in name and "metric" in name:
            return 0
        if "class" in name and "metric" in name:
            return 1
        if "metric" in name:
            return 2

    if target_type == "package":
        if "package" in name and "metric" in name:
            return 0
        if "metric" in name:
            return 2

    if "metric" in name:
        return 3

    return 99


def load_target_metrics(
    designite_dir: str | Path,
    target_name: str,
    target_type: str,
) -> dict[str, Any]:
    candidates = [
        p for p in _csv_files(designite_dir)
        if "metric" in p.name.lower()
    ]

    candidates = sorted(
        candidates,
        key=lambda p: _metric_file_priority(p, target_type),
    )

    for csv_path in candidates:
        try:
            rows = _read_csv_rows(csv_path)
        except Exception:
            continue

        for row in rows:
            if not _is_target_row(row, target_name):
                continue

            numeric_metrics: dict[str, int | float] = {}

            for key, value in row.items():
                num = _numeric(value)
                if num is not None:
                    numeric_metrics[key] = num

            return {
                "found": True,
                "source": csv_path.name,
                "row": row,
                "numeric": numeric_metrics,
            }

    return {
        "found": False,
        "source": "",
        "row": {},
        "numeric": {},
    }


def compare_target_metrics(
    before: dict[str, Any],
    after: dict[str, Any],
) -> dict[str, list[Any]]:
    before_values = before.get("numeric", {}) or {}
    after_values = after.get("numeric", {}) or {}

    keys = sorted(set(before_values) | set(after_values))

    result: dict[str, list[Any]] = {}

    for key in keys:
        result[key] = [
            before_values.get(key),
            after_values.get(key),
        ]

    return result