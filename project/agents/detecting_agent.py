import json
import os
import pandas as pd
from pathlib import Path
from .smells_detection.designite_runner import DesigniteRunner
from .smells_detection.metrics_parser import MetricsParser

from .smells_detection.god_component import GodComponentDetector
from .smells_detection.insufficient_modularization import InsufficientModularizationDetector
from .smells_detection.unstable_dependency import UnstableDependencyDetector

class DetectingAgent:

    def __init__(self, project_name, classes_path):
        self.project_name = project_name
        self.output_path = f"{os.getenv("OUTPUT_PATH")}/metrics/{project_name}"
        self.project_path = f"{os.getenv("REPOSITORIES_PATH")}/{project_name}"
        self.runner = DesigniteRunner(self.project_path, self.output_path, classes_path)

    def collect_metrics(self):
        try:
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
        except Exception as e:
            print(f"Error collecting metrics: {e}")
            raise

    def generate_prompts(self, smell_name, smell_definition):
        try:
            if smell_name == "God Component":
                list_of_prompt_files = GodComponentDetector(self.project_name).generate_prompts({
                    "smell_name": smell_name,
                    "smell_definition": smell_definition
                })
                
                print(f"Prompts for God Component from {self.project_path} generated.")
                return list_of_prompt_files
            elif smell_name == "Insufficient Modularization":
                list_of_prompt_files = InsufficientModularizationDetector(self.project_name).generate_prompts({
                    "smell_name": smell_name,
                    "smell_definition": smell_definition
                })

                print(f"Prompts for Insufficient Modularization from {self.project_path} generated.")
                return list_of_prompt_files
            elif smell_name == "Unstable Dependency":
                from .smells_detection.unstable_dependency import UnstableDependencyDetector
                list_of_prompt_files = UnstableDependencyDetector(self.project_name).generate_prompts({
                    "smell_name": smell_name,
                    "smell_definition": smell_definition
                })

                print(f"Prompts for Unstable Dependency from {self.project_path} generated.")
                return list_of_prompt_files
            else:
                print(f"Prompt generator for {smell_name} is not implemented yet.")
        except Exception as e:
            print(f"Error generating prompts for {smell_name}: {e}")
            raise
    
    def detect(self, smell_name, list_of_prompt_files):
        try:
            if smell_name == "God Component":
                GodComponentDetector(self.project_name).detect_gpt(list_of_prompt_files)
                #GodComponentDetector(self.project_name).detect_hf(list_of_prompt_files)
                print(f"God Component detection for {self.project_path} completed.")
            elif smell_name == "Insufficient Modularization":
                InsufficientModularizationDetector(self.project_name).detect_gpt(list_of_prompt_files)
                #InsufficientModularizationDetector(self.project_name).detect_hf(list_of_prompt_files)
                print(f"Insufficient Modularization detection for {self.project_path} completed.")
            elif smell_name == "Unstable Dependency":
                UnstableDependencyDetector(self.project_name).detect_gpt(list_of_prompt_files)
                #UnstableDependencyDetector(self.project_name).detect_hf(list_of_prompt_files)
                print(f"Unstable Dependency detection for {self.project_path} completed.")
            else:
                print(f"Smell detection for {smell_name} is not implemented yet.")
        except Exception as e:
            print(f"Error detecting smell {smell_name}: {e} for {self.project_path}")
            raise