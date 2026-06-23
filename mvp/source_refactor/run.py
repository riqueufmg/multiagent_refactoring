import argparse
import json
from pathlib import Path

import dotenv

from mvp.source_refactor.graph import build_source_refactor_graph


def main() -> None:
    dotenv.load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        required=True,
        help="Path to source_refactor MVP YAML config",
    )
    args = parser.parse_args()

    app = build_source_refactor_graph()

    out = app.invoke(
        {
            "config_path": str(Path(args.config).expanduser().resolve()),
        }
    )

    status = out.get("status", {})
    print(json.dumps(status, indent=2))

    if not status.get("ok", False):
        raise SystemExit(1)


if __name__ == "__main__":
    main()