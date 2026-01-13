import json
import os
from pathlib import Path
from utils.openrouter_engine import OpenRouterEngine


class InsufficientModularizationDetector:

    def __init__(self, project_name: str):
        self.project_name = project_name
        self.json_path = f"{os.getenv('OUTPUT_PATH')}/metrics/{project_name}/project_metrics.json"
        self.prompts_template_path = Path(
            "data/prompts/templates/detection_insufficient_modularization.tpl"
        )
        self.generated_prompts_dir = Path(
            "data/processed/prompts/insufficient_modularization"
        )
        self.engine = OpenRouterEngine(model="gpt-5-mini")

    def filter_data(self):
        if not Path(self.json_path).exists():
            raise FileNotFoundError(f"JSON file not found: {self.json_path}")

        with open(self.json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        full_class_map = self._build_class_map(data)

        result = []
        for cls_key, cls_obj in full_class_map.items():
            analyzed_class = {
                "key": cls_key,
                "package": cls_obj["package"],
                "class": cls_obj["class"],
                "file": cls_obj.get("file"),
            }

            result.append({
                "analyzed_class": analyzed_class
            })

        return result, full_class_map

    def _build_class_map(self, data):
        full_class_map = {}
        for package in data.get("packages", []):
            for cls in package.get("classes", []):
                key = f"{cls['package']}.{cls['class']}"
                full_class_map[key] = cls
        return full_class_map

    def _write_class_code(self, fp, cls_info):
        file_path = Path(cls_info.get("file", ""))
        if not file_path.exists():
            return

        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                code = f.read()
        except Exception:
            return

        fp.write(
            f"// ===== PACKAGE: {cls_info['package']}, CLASS: {cls_info['class']} =====\n"
        )
        fp.write(code + "\n\n")

    def generate_prompts(self) -> list[Path]:
        classes_data, _ = self.filter_data()

        if not self.prompts_template_path.exists():
            raise FileNotFoundError(
                f"Template not found: {self.prompts_template_path}"
            )

        with open(self.prompts_template_path, "r", encoding="utf-8") as f:
            template_content = f.read()

        list_of_prompts = []
        project_out_dir = self.generated_prompts_dir / self.project_name
        project_out_dir.mkdir(parents=True, exist_ok=True)

        for entry in classes_data:
            analyzed = entry["analyzed_class"]
            safe_name = f"{analyzed['package']}.{analyzed['class']}".replace(".", "_")
            prompt_file = project_out_dir / f"{safe_name}.txt"

            if prompt_file.exists():
                list_of_prompts.append(prompt_file)
                continue

            with open(prompt_file, "w", encoding="utf-8") as fp:
                fp.write("## Analyzed Class\n")
                self._write_class_code(fp, analyzed)

            with open(prompt_file, "r", encoding="utf-8") as fp_read:
                prompt_body = fp_read.read()

            total_tokens = self.engine.count_tokens(
                template_content.replace("{INPUT_DATA}", prompt_body)
            )

            with open(prompt_file, "w", encoding="utf-8") as fp:
                fp.write(f"##CONTEXT_SIZE={total_tokens}\n")
                fp.write(template_content.replace("{INPUT_DATA}", prompt_body))

            list_of_prompts.append(prompt_file)

        return list_of_prompts
