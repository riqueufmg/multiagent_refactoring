import subprocess
import pandas as pd
import json
from pathlib import Path
from collections import defaultdict

class DetectingAgent:

    ##
    # Initialize the DetectingAgent with project path, output path, and classes path.
    ##
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
    
    def collect_package_dependencies(self):
        cmd = [
            "jdeps",
            "-verbose:package",
            str(self.project_path)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        dependencies = defaultdict(list)

        if result.returncode != 0:
            print("Error running jdeps:", result.stderr)
            return {}

        for line in result.stdout.splitlines():
            line = line.strip()
            if "->" in line:
                source, target = line.split("->")
                source = source.strip()
                target = target.split()[0].strip()

                if source.startswith(("java.", "javax.")) or target.startswith(("java.", "javax.")):
                    continue

                if target not in dependencies[source]:
                    dependencies[source].append(target)

        return dict(dependencies)
    
    ##
    # Normalize DataFrame column names by stripping whitespace,
    # removing BOM characters, converting to lowercase, and replacing spaces with underscores.
    ##
    @staticmethod
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
    @staticmethod
    def parse_class_metrics(row):
        return {
            "package_name": row["package_name"],
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
    @staticmethod
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

    ##
    # Group classes by their package and aggregate metrics.
    ##
    @staticmethod
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
            }

            packages_list.append({
                "package_name": pkg_name,
                "metrics": pkg_metrics,
                "classes": classes,
                "dependencies": []
            })

        return packages_list

    ##
    # Attach methods to their corresponding classes within packages.
    ##
    @staticmethod
    def attach_methods_to_classes(packages, method_rows):
        class_index = {}
        for pkg in packages:
            for cls in pkg["classes"]:
                key = (pkg["package_name"], cls["class_name"])
                class_index[key] = cls

        for row in method_rows:
            pkg_name = row["package_name"]
            cls_name = row["type_name"]
            key = (pkg_name, cls_name)

            if key in class_index:
                cls_obj = class_index[key]
                method_obj = DetectingAgent.parse_method_metrics(row)

                cls_obj["methods"].append(method_obj)
            else:
                print(f"Warning: Class {cls_name} in package {pkg_name} not found for method {row.get('method_name')}")

        return packages
    
    @staticmethod
    def attach_package_dependencies(packages, package_dependencies):
        package_index = {
            pkg["package_name"]: pkg
            for pkg in packages
        }

        for source_pkg, targets in package_dependencies.items():
            if source_pkg in package_index:
                package_index[source_pkg]["dependencies"].extend(targets)
            else:
                # Opcional: pode logar para debug
                print(f"Warning: Package {source_pkg} not found in project structure")

        return packages
    
    ##
    # Collect metrics by running Designite and processing the output CSV files.
    ##
    def collect_metrics(self):
        self.run_designite()

        class_csv = Path(self.output_path) / "TypeMetrics.csv"
        method_csv = Path(self.output_path) / "MethodMetrics.csv"

        class_df = pd.read_csv(class_csv)
        method_df = pd.read_csv(method_csv)

        class_df, _ = self.normalize_columns(class_df)
        method_df, _ = self.normalize_columns(method_df)

        class_dicts = [self.parse_class_metrics(row) for _, row in class_df.iterrows()]
        packages = self.group_classes_by_package(class_dicts)

        method_rows = method_df.to_dict(orient="records") ## convert df to list of dicts
        packages = self.attach_methods_to_classes(packages, method_rows)

        package_dependencies = self.collect_package_dependencies()
        packages = self.attach_package_dependencies(packages, package_dependencies)

        final_json = {
            "project": Path(self.project_path).name,
            "summary": {
                "total_packages": len(packages),
                "total_classes": sum(len(p["classes"]) for p in packages)
            },
            "packages": packages
        }

        output_file = Path(self.output_path) / "project_metrics.json"
        with open(output_file, "w") as f:
            json.dump(final_json, f, indent=4)

        print(f"Metrics collected and saved to {output_file}")
        return final_json

    ##
    # Main run method to execute the agent's functionality.
    ##
    def run(self):
        #self.collect_metrics()
        self.collect_package_dependencies()
        print("DetectingAgent run method executed.")