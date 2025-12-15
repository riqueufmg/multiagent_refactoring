import subprocess
import pandas as pd
from pathlib import Path
from collections import defaultdict

class DetectingAgent:

    def __init__(self, project_path, output_path, classes_path):
        self.project_path = project_path
        self.output_path = output_path
        self.classes_path = classes_path

    ##
    # Run DesigniteJava tool to analyze the Java project.
    ##
    def run_designite(self):
        
        Path(self.output_path).mkdir(parents=True, exist_ok=True)
        
        cmd = [
            "java", "-jar", "tools/DesigniteJava.jar",
            "-i", self.project_path,
            "-o", self.output_path,
            "-c", self.classes_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)

        print(result.stdout)
        print(result.stderr)
    
    ##
    # Normalize DataFrame column names by stripping whitespace,
    # removing BOM characters, converting to lowercase, and replacing spaces with underscores.
    ##
    def normalize_columns(df):
        old_cols = df.columns
        new_cols = []
        mapping = {}

        for c in old_cols:
            clean = c.strip().replace("\ufeff", "")
            normalized = clean.lower().replace(" ", "_")
            new_cols.append(normalized)
            mapping[normalized] = clean

        df.columns = new_cols
        return df, mapping
    
    ##
    # Parse class metrics from a DataFrame row into a dictionary.
    ##
    def parse_class_metrics(row):
        return {
            "class_name": row["type_name"],
            "file_path": row.get("file_path"),
            "line_no": int(row.get("line_no", -1)),
            "metrics": {
                "nof": int(row.get("nof", 0)),
                "nopf": int(row.get("nopf", 0)),
                "nom": int(row.get("nom", 0)),
                "nopm": int(row.get("nopm", 0)),
                "loc": int(row.get("loc", 0)),
                "wmc": int(row.get("wmc", 0)),
                "nc": int(row.get("nc", 0)),
                "dit": int(row.get("dit", 0)),
                "lcom": float(row.get("lcom", 0)),
                "fanin": int(row.get("fanin", 0)),
                "fanout": int(row.get("fanout", 0)),
            },
            "methods": [],
            "dependencies": []
        }

    ##
    # Parse method metrics from a DataFrame row into a dictionary.
    ##
    def parse_method_metrics(row):
        return {
            "method_name": row["method_name"],
            "line_no": int(row.get("line_no", -1)),
            "is_test": bool(int(row.get("is_test", 0))) if "is_test" in row else False,
            "main_prod_class_tested": row.get("main_prod_class_tested"),
            "production_classes_tested": row.get("production_classes_tested"),
            "metrics": {
                "loc": int(row.get("loc", 0)),
                "cc": int(row.get("cc", 0)),
                "pc": int(row.get("pc", 0)),
                "fanin": int(row.get("fanin", 0)) if "fanin" in row else None,
                "fanout": int(row.get("fanout", 0)) if "fanout" in row else None,
            },
            "dependencies": []
        }

    def group_classes_by_package(class_rows):
        packages_dict = defaultdict(list)

        for cls in class_rows:
            package_name = cls.get("package_name", "default_package")
            packages_dict[package_name].append(cls)

        packages_list = []
        for pkg_name, classes in packages_dict.items():
            pkg_metrics = {
                "num_classes": len(classes),
                "loc": sum(c["metrics"]["loc"] for c in classes),
                "wmc": sum(c["metrics"]["wmc"] for c in classes),
                "fanin": sum(c["metrics"]["fanin"] for c in classes),
                "fanout": sum(c["metrics"]["fanout"] for c in classes),
            }

            packages_list.append({
                "package_name": pkg_name,
                "metrics": pkg_metrics,
                "classes": classes
            })

        return packages_list
    
    def collect_metrics(self):
        self.run_designite()

    def run(self):
        self.collect_metrics()
        print("DetectingAgent run method executed.")