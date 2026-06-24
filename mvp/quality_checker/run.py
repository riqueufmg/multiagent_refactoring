from __future__ import annotations

import argparse
from pathlib import Path

from mvp.quality_checker.graph import build_quality_checker_graph


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        required=True,
        help="Path to quality_checker config.yml",
    )

    args = parser.parse_args()

    app = build_quality_checker_graph()

    out = app.invoke(
        {
            "config_path": str(Path(args.config).expanduser().resolve()),
        }
    )

    status = out.get("status", {})
    ok = status.get("ok", False)

    print(f"quality_checker ok={ok}")
    print(f"status={status.get('status_path', '')}")


if __name__ == "__main__":
    main()