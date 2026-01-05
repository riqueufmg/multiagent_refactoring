import pandas as pd
import json
from collections import defaultdict
from pathlib import Path
import xml.etree.ElementTree as ET

class MetricsParser:
    
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

    @staticmethod
    def parse_class_metrics(row, project_path):
        return {
            "package": row["package"],
            "class": row["class"],
            "file": row.get("file")[row.get("file").index(project_path):] if row.get("file") else "",
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
            "dependencies": []
        }

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
                "Ce": 0,
                "Ca": 0,
            }

            packages_list.append({
                "package": pkg_name,
                "metrics": pkg_metrics,
                "classes": classes,
                "dependencies": []
            })

        return packages_list

    @staticmethod
    def classname_to_package(class_name):
        parts = class_name.split(".")
        while parts and parts[-1][0].isupper():
            parts.pop()
        return ".".join(parts)

    @staticmethod
    def parser_dependencies(graph_path):
        tree = ET.parse(graph_path)
        root = tree.getroot()
        ns = {"g": "http://graphml.graphdrawing.org/xmlns"}

        package_dependencies = defaultdict(set)
        class_dependencies = defaultdict(set)

        for edge in root.findall(".//g:edge", ns):
            source_pkg = MetricsParser.classname_to_package(edge.attrib["source"])
            target_pkg = MetricsParser.classname_to_package(edge.attrib["target"])

            if source_pkg != target_pkg:
                package_dependencies[source_pkg].add(target_pkg)

            source_class = edge.attrib["source"]
            target_class = edge.attrib["target"]

            if source_class != target_class:
                class_dependencies[source_class].add(target_class)

        package_dependencies = {k: list(v) for k, v in package_dependencies.items()}
        class_dependencies = {k: list(v) for k, v in class_dependencies.items()}

        return package_dependencies, class_dependencies

    @staticmethod
    def calculate_afferent_coupling(package_dependencies):
        afferent = defaultdict(int)
        for source_pkg, targets in package_dependencies.items():
            for target_pkg in targets:
                afferent[target_pkg] += 1
        return dict(afferent)

    '''@staticmethod
    def attach_dependencies(packages, package_dependencies, class_dependencies):
        package_index = {pkg["package"]: pkg for pkg in packages}
        valid_classes = {f'{pkg["package"]}.{cls["class"]}' for pkg in packages for cls in pkg["classes"]}

        for source_pkg, targets in package_dependencies.items():
            if source_pkg in package_index:
                deps = set(package_index[source_pkg]["dependencies"])
                deps.update(targets)
                package_index[source_pkg]["dependencies"] = list(deps)
                package_index[source_pkg]["metrics"]["Ce"] = len(deps)

        afferent_coupling = MetricsParser.calculate_afferent_coupling(package_dependencies)

        for pkg_name, pkg in package_index.items():
            pkg["metrics"]["Ca"] = afferent_coupling.get(pkg_name, 0)

        for pkg in packages:
            for cls_obj in pkg["classes"]:
                class_name = f'{pkg["package"]}.{cls_obj["class"]}'
                raw_deps = class_dependencies.get(class_name, [])
                cls_obj["dependencies"] = [dep for dep in raw_deps if dep in valid_classes]

        return packages'''
    
    @staticmethod
    def attach_dependencies(packages, package_dependencies, class_dependencies):
        package_index = {pkg["package"]: pkg for pkg in packages}
        
        valid_classes = {f'{pkg["package"]}.{cls["class"]}' for pkg in packages for cls in pkg["classes"]}

        for source_pkg, targets in package_dependencies.items():
            if source_pkg in package_index:
                valid_targets = [t for t in targets if t in package_index]  # somente pacotes válidos
                package_index[source_pkg]["dependencies"] = valid_targets
                package_index[source_pkg]["metrics"]["Ce"] = len(valid_targets)

        afferent_coupling = defaultdict(int)
        for source_pkg, targets in package_dependencies.items():
            for target_pkg in targets:
                if target_pkg in package_index and source_pkg in package_index:
                    afferent_coupling[target_pkg] += 1

        for pkg_name, pkg in package_index.items():
            pkg["metrics"]["Ca"] = afferent_coupling.get(pkg_name, 0)

        for pkg in packages:
            for cls_obj in pkg["classes"]:
                class_name = f'{pkg["package"]}.{cls_obj["class"]}'
                raw_deps = class_dependencies.get(class_name, [])
                cls_obj["dependencies"] = [dep for dep in raw_deps if dep in valid_classes]

        return packages