import pandas as pd
import json
from pathlib import Path
from .smells_detection.designite_runner import DesigniteRunner
from .smells_detection.metrics_parser import MetricsParser

class DetectingAgent:

    def __init__(self, project_path, output_path, classes_path, jar_path):
        self.runner = DesigniteRunner(project_path, output_path, classes_path, jar_path)
        self.output_path = output_path
        self.project_path = project_path

    def collect_metrics(self):
        self.runner.run()

        class_csv = Path(self.output_path) / "TypeMetrics.csv"
        method_csv = Path(self.output_path) / "MethodMetrics.csv"
        graph_path = Path(self.output_path) / "DependencyGraph.graphml"

        class_df = pd.read_csv(class_csv)
        class_df, _ = MetricsParser.normalize_columns(class_df)

        class_dicts = [
            MetricsParser.parse_class_metrics(row, self.project_path)
            for _, row in class_df.iterrows()
            if "/test/" not in row.get("file", "")
        ]

        packages = MetricsParser.group_classes_by_package(class_dicts)
        package_dependencies, class_dependencies = MetricsParser.parser_dependencies(graph_path)
        packages = MetricsParser.attach_dependencies(packages, package_dependencies, class_dependencies)

        final_json = {
            "project": Path(self.project_path).name,
            "summary": {
                "total_packages": len(packages),
                "total_classes": sum(len(p["classes"]) for p in packages)
            },
            "packages": packages
        }

        output_file = Path(self.output_path, "project_metrics.json")
        with open(output_file, "w") as f:
            json.dump(final_json, f, indent=4)

        print(f"Metrics collected and saved to {output_file}")
        return final_json
