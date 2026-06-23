import argparse
import json
from pathlib import Path

import dotenv

from mvp.planner.graph import build_planner_graph

def main() -> None:
    dotenv.load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Path to planner MVP YAML config")
    args = parser.parse_args()

    app = build_planner_graph()

    out = app.invoke(
        {
            "config_path": str(Path(args.config).resolve()),
        }
    )

    status = out.get("status", {})
    print(json.dumps(status, indent=2))

    if not status.get("ok", False):
        raise SystemExit(1)


if __name__ == "__main__":
    main()