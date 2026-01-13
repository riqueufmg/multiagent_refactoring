import json
import os
from pathlib import Path
from utils.openrouter_engine import OpenRouterEngine


class GodComponentDetector:

    def __init__(self, project_name: str):
        self.project_name = project_name
        self.json_path = f"{os.getenv('OUTPUT_PATH')}/metrics/{project_name}/project_metrics.json"
        self.prompts_template_path = Path(
            "data/prompts/templates/detection_god_component.tpl"
        )
        self.generated_prompts_dir = Path(
            "data/processed/prompts/god_component"
        )
        self.engine = OpenRouterEngine(model="gpt-5-mini")

    def filter_data(self):
        if not Path(self.json_path).exists():
            raise FileNotFoundError(f"JSON file not found: {self.json_path}")

        with open(self.json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        packages_list = []
        for pkg in data.get("packages", []):
            packages_list.append({
                "package": pkg["package"],
                "classes": pkg.get("classes", [])
            })

        return packages_list

    def _collect_package_code(self, package_info: dict) -> list[str]:
        code_blocks = []
        for cls in package_info["classes"]:
            file_path = Path(cls["file"])
            if not file_path.exists():
                continue

            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    code = f.read()
            except Exception:
                continue

            code_blocks.append(f"// ===== PACKAGE: {cls['package']}, CLASS: {cls['class']} =====\n{code}")

        return code_blocks

    def generate_prompts(self) -> list[Path]:
        packages = self.filter_data()

        if not self.prompts_template_path.exists():
            raise FileNotFoundError(f"Template not found: {self.prompts_template_path}")

        with open(self.prompts_template_path, "r", encoding="utf-8") as f:
            template_content = f.read()

        list_of_prompts = []
        project_out_dir = self.generated_prompts_dir / self.project_name
        project_out_dir.mkdir(parents=True, exist_ok=True)

        for pkg in packages:
            safe_pkg_name = pkg["package"].replace(".", "_")
            prompt_file = project_out_dir / f"{safe_pkg_name}.txt"

            if prompt_file.exists():
                list_of_prompts.append(prompt_file)
                continue

            with open(prompt_file, "w", encoding="utf-8") as fp:
                fp.write("## Analyzed Package\n")
                for cls_code in self._collect_package_code(pkg):
                    fp.write(cls_code + "\n\n")

            with open(prompt_file, "r", encoding="utf-8") as fp_read:
                prompt_body = fp_read.read()
            total_tokens = self.engine.count_tokens(template_content.replace("{INPUT_DATA}", prompt_body))

            with open(prompt_file, "w", encoding="utf-8") as fp:
                fp.write(f"##CONTEXT_SIZE={total_tokens}\n")
                fp.write(template_content.replace("{INPUT_DATA}", prompt_body))

            list_of_prompts.append(prompt_file)

        return list_of_prompts
