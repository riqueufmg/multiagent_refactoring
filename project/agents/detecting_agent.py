import subprocess
import pandas as pd
import json
from pathlib import Path
from collections import defaultdict
import xml.etree.ElementTree as ET

class DetectingAgent:

    ##
    # Initialize the DetectingAgent with project path, output path, and classes path.
    ##
    def __init__(self, project_path, output_path, classes_path, jar_path):
        self.project_path = project_path
        self.output_path = output_path
        self.classes_path = classes_path
        self.jar_path = jar_path

    ##
    # Run DesigniteJava tool to analyze the Java project.
    ##
    def run_designite(self):
        
        Path(self.output_path).mkdir(parents=True, exist_ok=True)
        
        cmd = [
            "java", "-jar", "tools/DesigniteJava2.8.0.jar",
            "-i", self.project_path,
            "-o", self.output_path,
            "-c", self.classes_path,
            "-g",
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
    
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
            "package": row["package"],
            "class": row["class"],
            "file": row.get("file"),
            #"line_no": int(row.get("line_no", -1)),
            "metrics": {
                "nof": int(row.get("nof", 0)),
                #"nopf": int(row.get("nopf", 0)),
                "nom": int(row.get("nom", 0)),
                "nopm": int(row.get("nopm", 0)),
                "loc": int(row.get("loc", 0)),
                "wmc": int(row.get("wmc", 0)),
                #"nc": int(row.get("nc", 0)),
                #"dit": int(row.get("dit", 0)),
                #"lcom": float(row.get("lcom", 0)),
                #"fanin": int(row.get("fanin", 0)),
                #"fanout": int(row.get("fanout", 0)),
            },
            #"methods": [],
            "dependencies": []
        }

    ##
    # Parse method metrics from a DataFrame row into a dictionary.
    ##
    @staticmethod
    def parse_method_metrics(row):
        return {
            "method": row["method"],
            "line_no": int(row.get("line_no", -1)),
            "is_test": bool(int(row["is_test"])) if "is_test" in row and pd.notna(row["is_test"]) else False,
            "main_prod_class_tested": row.get("main_prod_class_tested"),
            "production_classes_tested": row.get("production_classes_tested"),
            "metrics": {
                "loc": int(row.get("loc", 0)),
                "cc": int(row.get("cc", 0)),
                "pc": int(row.get("pc", 0)),
                "fanin": int(row.get("fanin", 0)) if "fanin" in row else None,
                "fanout": int(row.get("fanout", 0)) if "fanout" in row else None,
            },
            #"dependencies": []
        }

    ##
    # Group classes by their package and aggregate metrics.
    ##
    @staticmethod
    def group_classes_by_package(class_rows):
        packages_dict = defaultdict(list)

        for cls in class_rows:
            package = cls.get("package", "default_package")
            packages_dict[package].append(cls)

        packages_list = []
        for pkg_name, classes in packages_dict.items():
            pkg_metrics = {
                "num_classes": len(classes),
                "loc": sum(c["metrics"]["loc"] for c in classes),
                "efferent_coupling": 0,
                "afferent_coupling": 0,
            }

            packages_list.append({
                "package": pkg_name,
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
                key = (pkg["package"], cls["class"])
                class_index[key] = cls

        for row in method_rows:
            pkg_name = row["package"]
            cls_name = row["class"]
            key = (pkg_name, cls_name)

            if key in class_index:
                cls_obj = class_index[key]
                method_obj = DetectingAgent.parse_method_metrics(row)

                cls_obj["methods"].append(method_obj)
            #else:
                #print(f"Warning: Class {cls_name} in package {pkg_name} not found for method {row.get('method')}")

        return packages
    
    ##
    # Convert a fully qualified class name to its package name.
    ##
    @staticmethod
    def classname_to_package(class_name):
        parts = class_name.split(".")
        while parts and parts[-1][0].isupper():
            parts.pop()
        return ".".join(parts)
    
    ##
    # Parse dependencies from the GraphML file generated by Designite.
    ##
    @staticmethod
    def parser_dependencies(graph_path):
        tree = ET.parse(graph_path)
        root = tree.getroot()

        ns = {"g": "http://graphml.graphdrawing.org/xmlns"}

        package_dependencies = defaultdict(set)
        class_dependencies = defaultdict(set)

        for edge in root.findall(".//g:edge", ns):
            source_pkg = DetectingAgent.classname_to_package(edge.attrib["source"])
            target_pkg = DetectingAgent.classname_to_package(edge.attrib["target"])

            if source_pkg != target_pkg:
                package_dependencies[source_pkg].add(target_pkg)
            
            source_class = edge.attrib["source"]
            target_class = edge.attrib["target"]

            if source_class != target_class:
                class_dependencies[source_class].add(target_class)
        
        package_dependencies = {k: list(v) for k, v in package_dependencies.items()}
        class_dependencies = {k: list(v) for k, v in class_dependencies.items()}
        
        return package_dependencies, class_dependencies
    
    ##
    # Calculate afferent coupling for packages based on dependencies.
    ##
    @staticmethod
    def calculate_afferent_coupling(package_dependencies):
        afferent = defaultdict(int)

        for source_pkg, targets in package_dependencies.items():
            for target_pkg in targets:
                afferent[target_pkg] += 1

        return dict(afferent)
    
    ##
    # Attach dependencies to packages and classes.
    ##
    @staticmethod
    def attach_dependencies(packages, package_dependencies, class_dependencies):
        package_index = {pkg["package"]: pkg for pkg in packages}

        for source_pkg, targets in package_dependencies.items():
            if source_pkg in package_index:
                deps = set(package_index[source_pkg]["dependencies"])
                deps.update(targets)

                package_index[source_pkg]["dependencies"] = list(deps)
                package_index[source_pkg]["metrics"]["efferent_coupling"] = len(deps)
            #else:
                #print(f"Warning: Package {source_pkg} not found in project structure")
        
        afferent_coupling = DetectingAgent.calculate_afferent_coupling(package_dependencies)

        for pkg_name, pkg in package_index.items():
            ca = afferent_coupling.get(pkg_name, 0)
            pkg["metrics"]["afferent_coupling"] = ca

            ce = pkg["metrics"].get("efferent_coupling", 0)

            # Calculate instability metric
            if ce + ca > 0:
                pkg["metrics"]["instability"] = ce / (ce + ca)
            else:
                pkg["metrics"]["instability"] = 0.0

        for pkg in packages:
            for cls_obj in pkg["classes"]:
                class_name = f'{pkg["package"]}.{cls_obj["class"]}'

                if class_name in class_dependencies:
                    cls_obj["dependencies"] = class_dependencies[class_name]
                else:
                    cls_obj["dependencies"] = []


        return packages
    
    ##
    # Collect metrics by running Designite and processing the output CSV files.
    ##
    def collect_metrics(self):
        self.run_designite()

        class_csv = Path(self.output_path) / "TypeMetrics.csv"
        method_csv = Path(self.output_path) / "MethodMetrics.csv"
        graph_path = Path(self.output_path) / "DependencyGraph.graphml"

        class_df = pd.read_csv(class_csv)
        method_df = pd.read_csv(method_csv)

        class_df, _ = self.normalize_columns(class_df)
        method_df, _ = self.normalize_columns(method_df)

        #class_dicts = [self.parse_class_metrics(row) for _, row in class_df.iterrows()]
        class_dicts = []
        for _, row in class_df.iterrows():
            class_dict = self.parse_class_metrics(row)
            if "/test/" not in class_dict["file"]:
                class_dicts.append(class_dict)

        packages = self.group_classes_by_package(class_dicts)

        #method_rows = method_df.to_dict(orient="records") ## convert df to list of dicts
        #packages = self.attach_methods_to_classes(packages, method_rows)

        package_dependencies, class_dependencies = self.parser_dependencies(graph_path)

        packages = self.attach_dependencies(packages, package_dependencies, class_dependencies)

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
        self.collect_metrics()
        print("DetectingAgent run method executed.")