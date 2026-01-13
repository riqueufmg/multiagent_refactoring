import json
import os
from pathlib import Path
from utils.openrouter_engine import OpenRouterEngine

class UnstableDependencyDetector:
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.json_path = f"{os.getenv('OUTPUT_PATH')}/metrics/{project_name}/project_metrics.json"
        self.prompts_template_path = Path(
            "data/prompts/templates/detection_unstable_dependency.tpl"
        )
        self.generated_prompts_dir = Path(
            "data/processed/prompts/unstable_dependency"
        )
        self.engine = OpenRouterEngine(
            model="gpt-5-mini"
        )
        self._package_code_cache = {}

    def filter_data(self):
        if not Path(self.json_path).exists():
            raise FileNotFoundError(f"JSON file not found: {self.json_path}")

        with open(self.json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        packages_index = {pkg["package"]: pkg for pkg in data.get("packages", [])}

        outgoing_map = {}
        for pkg_name, pkg in packages_index.items():
            outgoing_map[pkg_name] = list(set(pkg.get("dependencies", [])))

        incoming_map = {pkg_name: [] for pkg_name in packages_index}
        for src, targets in outgoing_map.items():
            for target in targets:
                if target in incoming_map:
                    incoming_map[target].append(src)

        filtered_packages = []
        for pkg_name in packages_index:
            filtered_packages.append({
                "analyzed_package": pkg_name,
                "outgoing": outgoing_map.get(pkg_name, []),
                "incoming": incoming_map.get(pkg_name, [])
            })

        return filtered_packages, packages_index

    def _collect_package_code(self, package_name: str, packages_index: dict, include_header: bool = True) -> list[str]:
        if package_name in self._package_code_cache:
            return self._package_code_cache[package_name]

        code_blocks = []
        pkg = packages_index.get(package_name)
        if not pkg:
            return []

        for cls in pkg.get("classes", []):
            raw_path = cls.get("file")
            if not raw_path:
                continue

            cleaned_path = Path(raw_path)
            if cleaned_path.exists():
                try:
                    with open(cleaned_path, "r", encoding="utf-8", errors="ignore") as f:
                        code = f.read()
                        if include_header:
                            code_blocks.append(f"// ===== PACKAGE: {cls['package']}, CLASS: {cls['class']} =====\n{code}")
                        else:
                            code_blocks.append(code)
                except Exception:
                    continue

        self._package_code_cache[package_name] = code_blocks
        return code_blocks

    def generate_prompts(self) -> list[Path]:
        packages_data, packages_index = self.filter_data()

        if not self.prompts_template_path.exists():
            raise FileNotFoundError(f"Template not found: {self.prompts_template_path}")

        with open(self.prompts_template_path, "r", encoding="utf-8") as f:
            template_content = f.read()

        list_of_prompts = []
        project_out_dir = self.generated_prompts_dir / self.project_name
        project_out_dir.mkdir(parents=True, exist_ok=True)

        for pkg_entry in packages_data:
            analyzed_pkg = pkg_entry["analyzed_package"]
            safe_pkg_name = analyzed_pkg.replace(".", "_")
            prompt_file = project_out_dir / f"{safe_pkg_name}.txt"

            if prompt_file.exists():
                list_of_prompts.append(prompt_file)
                continue

            with open(prompt_file, "w", encoding="utf-8") as fp:

                fp.write("## Analyzed Package Classes\n")
                for cls_code in self._collect_package_code(analyzed_pkg, packages_index, include_header=True):
                    fp.write(cls_code + "\n\n")

                dependency_roles = {}
                for pkg_name in pkg_entry["outgoing"]:
                    dependency_roles[pkg_name] = {"OUTGOING"}
                for pkg_name in pkg_entry["incoming"]:
                    dependency_roles.setdefault(pkg_name, set()).add("INCOMING")

                if dependency_roles:
                    fp.write("## Dependent Package Classes\n")

                for dep_pkg in dependency_roles.keys():
                    for cls_code in self._collect_package_code(dep_pkg, packages_index, include_header=True):
                        fp.write(cls_code + "\n\n")

            with open(prompt_file, "r", encoding="utf-8") as fp_read:
                prompt_body = fp_read.read()
            total_tokens = self.engine.count_tokens(template_content.replace("{INPUT_DATA}", prompt_body))

            with open(prompt_file, "w", encoding="utf-8") as fp:
                fp.write(f"##CONTEXT_SIZE={total_tokens}\n")
                fp.write(template_content.replace("{INPUT_DATA}", prompt_body))

            list_of_prompts.append(prompt_file)

        return list_of_prompts