import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def start_llm_timer() -> dict[str, Any]:
    return {
        "started_at": utc_now_iso(),
        "_perf_counter": time.perf_counter(),
    }


def build_llm_usage_entry(
    *,
    timer: dict[str, Any],
    agent: str,
    model: str,
    response: Any,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    finished_at = utc_now_iso()
    duration_seconds = time.perf_counter() - float(timer["_perf_counter"])

    usage_metadata = getattr(response, "usage_metadata", None) or {}
    response_metadata = getattr(response, "response_metadata", None) or {}

    token_usage = {}
    if isinstance(response_metadata, dict):
        token_usage = response_metadata.get("token_usage", {}) or {}

    input_tokens = (
        usage_metadata.get("input_tokens")
        or token_usage.get("prompt_tokens")
        or token_usage.get("input_tokens")
        or 0
    )

    output_tokens = (
        usage_metadata.get("output_tokens")
        or token_usage.get("completion_tokens")
        or token_usage.get("output_tokens")
        or 0
    )

    total_tokens = (
        usage_metadata.get("total_tokens")
        or token_usage.get("total_tokens")
        or input_tokens + output_tokens
    )

    return {
        "agent": agent,
        "model": model,
        "started_at": timer["started_at"],
        "finished_at": finished_at,
        "duration_seconds": round(duration_seconds, 3),
        "input_tokens": int(input_tokens or 0),
        "output_tokens": int(output_tokens or 0),
        "total_tokens": int(total_tokens or 0),
        "metadata": metadata or {},
        "usage_metadata": usage_metadata,
        "response_metadata": response_metadata,
    }


def append_llm_usage(
    *,
    usage_file: str | Path,
    entry: dict[str, Any],
) -> None:
    usage_path = Path(usage_file)
    usage_path.parent.mkdir(parents=True, exist_ok=True)

    if usage_path.exists():
        try:
            data = json.loads(usage_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            data = {"inferences": []}
    else:
        data = {"inferences": []}

    if not isinstance(data, dict):
        data = {"inferences": []}

    if "inferences" not in data or not isinstance(data["inferences"], list):
        data["inferences"] = []

    data["inferences"].append(entry)

    data["summary"] = summarize_llm_usage(data["inferences"])

    usage_path.write_text(
        json.dumps(data, indent=2),
        encoding="utf-8",
    )


def summarize_llm_usage(entries: list[dict[str, Any]]) -> dict[str, Any]:
    total_input_tokens = sum(int(e.get("input_tokens") or 0) for e in entries)
    total_output_tokens = sum(int(e.get("output_tokens") or 0) for e in entries)
    total_tokens = sum(int(e.get("total_tokens") or 0) for e in entries)
    total_duration_seconds = sum(float(e.get("duration_seconds") or 0) for e in entries)

    by_agent: dict[str, dict[str, Any]] = {}

    for entry in entries:
        agent = str(entry.get("agent") or "unknown")

        if agent not in by_agent:
            by_agent[agent] = {
                "calls": 0,
                "input_tokens": 0,
                "output_tokens": 0,
                "total_tokens": 0,
                "duration_seconds": 0.0,
            }

        by_agent[agent]["calls"] += 1
        by_agent[agent]["input_tokens"] += int(entry.get("input_tokens") or 0)
        by_agent[agent]["output_tokens"] += int(entry.get("output_tokens") or 0)
        by_agent[agent]["total_tokens"] += int(entry.get("total_tokens") or 0)
        by_agent[agent]["duration_seconds"] += float(entry.get("duration_seconds") or 0)

    for agent_summary in by_agent.values():
        agent_summary["duration_seconds"] = round(
            agent_summary["duration_seconds"],
            3,
        )

    return {
        "calls": len(entries),
        "input_tokens": total_input_tokens,
        "output_tokens": total_output_tokens,
        "total_tokens": total_tokens,
        "duration_seconds": round(total_duration_seconds, 3),
        "by_agent": by_agent,
    }