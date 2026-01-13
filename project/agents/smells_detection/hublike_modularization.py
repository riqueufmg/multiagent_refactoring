import json
from pathlib import Path
import os
import tiktoken

from agents.llm_inference.gpt_engine import GPTEngine
from agents.llm_inference.deepseek_engine import DeepSeekEngine
from agents.llm_inference.openrouter_engine import OpenRouterEngine

class HublikeModularizationDetector:

    def __init__(self, project_name):
        self.project_name = project_name
        self.json_path = (
            f"{os.getenv('OUTPUT_PATH')}/metrics/{project_name}/project_metrics.json"
        )
        self.prompts_path = os.getenv("PROMPTS_PATH")

    @staticmethod
    def count_tokens(text: str) -> int:
        encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(text))

    def filter_data(self):
        if not Path(self.json_path).exists():
            raise FileNotFoundError(f"JSON file not found: {self.json_path}")

        with open(self.json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        full_class_map = self._build_class_map(data)

        result = []
        for cls_key, cls_obj in full_class_map.items():
            analyzed_package = {
                "package": cls_obj["package"],
                "class": cls_obj["class"],
                "dependencies": cls_obj.get("dependencies", [])
            }

            outgoing = self._get_outgoing_dependencies(cls_obj, full_class_map)
            incoming = self._get_incoming_dependencies(cls_key, full_class_map)

            result.append({
                "analyzed_package": analyzed_package,
                "outgoing_dependencies": outgoing,
                "incoming_dependencies": incoming
            })

        return result

    def _build_class_map(self, data):
        full_class_map = {}
        for package in data.get("packages", []):
            for cls in package.get("classes", []):
                key = f"{cls['package']}.{cls['class']}"
                full_class_map[key] = cls
        return full_class_map

    def _get_outgoing_dependencies(self, cls_obj, full_class_map):
        outgoing = []
        for dep in cls_obj.get("dependencies", []):
            dep_obj = full_class_map.get(dep)
            if dep_obj:
                outgoing.append({
                    "package": dep_obj["package"],
                    "class": dep_obj["class"],
                    "dependencies": dep_obj.get("dependencies", [])
                })
        return outgoing

    def _get_incoming_dependencies(self, cls_key, full_class_map):
        incoming = []
        for other_key, other_obj in full_class_map.items():
            if cls_key in other_obj.get("dependencies", []):
                incoming.append({
                    "package": other_obj["package"],
                    "class": other_obj["class"],
                    "dependencies": other_obj.get("dependencies", [])
                })
        return incoming

    def generate_prompts(self, smell=None):
        classes_data = self.filter_data()

        template_file = Path(
            self.prompts_path,
            "templates",
            "detection_hublike_modularization.tpl"
        )
        if not template_file.exists():
            raise FileNotFoundError(f"Template file not found: {template_file}")

        with open(template_file, "r", encoding="utf-8") as f:
            template_content = f.read()

        list_of_prompt_files = []

        for cls_data in classes_data:
            input_data = json.dumps(cls_data, indent=2)
            prompt_body = template_content.replace("{INPUT_DATA}", input_data)

            body_token_count = self.count_tokens(prompt_body)
            header = f"##CONTEXT_SIZE={body_token_count}\n\n"
            prompt = header + prompt_body

            output_dir = Path(
                os.getenv("OUTPUT_PATH"),
                "prompts",
                "smell_detection",
                "hublike_modularization",
                self.project_name
            )
            output_dir.mkdir(parents=True, exist_ok=True)

            cls_name = cls_data["analyzed_package"]["class"]
            pkg_name = cls_data["analyzed_package"]["package"].replace("/", "_")
            prompt_file = output_dir / f"{pkg_name}_{cls_name}.txt"

            with open(prompt_file, "w", encoding="utf-8") as f:
                f.write(prompt)

            list_of_prompt_files.append(prompt_file)

        return list_of_prompt_files

    def detect_gpt(self, list_of_prompt_files):
        llm_config = {
            "model_name": "gpt-5-mini",
            "max_input_tokens": 100000,
            "max_completion_tokens": 30720
        }

        llm_engine = GPTEngine(**llm_config)

        output_base_dir = Path(
            "data",
            "processed",
            "llm_outputs",
            self.project_name,
            "hublike_modularization",
            "gpt"
        )
        output_base_dir.mkdir(parents=True, exist_ok=True)

        for prompt_file in list_of_prompt_files:
            output_file = output_base_dir / f"{prompt_file.stem}.txt"

            if output_file.exists():
                print(f"[SKIP] Output already exists: {output_file.name}")
                continue

            with open(prompt_file, "r", encoding="utf-8") as f:
                prompt_content = f.read()

            token_count = self.count_tokens(prompt_content)
            if token_count > 100_000:
                print(
                    f"[SKIP] {prompt_file.name} "
                    f"(CONTEXT_SIZE={token_count} > 100k)"
                )
                continue

            response = llm_engine.generate(prompt_content)

            tmp_file = output_file.with_suffix(".tmp")
            with open(tmp_file, "w", encoding="utf-8") as out_f:
                out_f.write(response)
            tmp_file.replace(output_file)

            print(f"[OK] Saved output to {output_file.name}")

    def detect_deepseek(self, list_of_prompt_files):
        llm_config = {
            "model_name": "deepseek-chat",
            "max_input_tokens": 100000,
            "max_completion_tokens": 8192,
        }

        llm_engine = DeepSeekEngine(**llm_config)

        output_dir = Path(
            os.getenv("OUTPUT_PATH"),
            "llm_outputs",
            self.project_name,
            "hublike_modularization",
            "deepseek"
        )
        output_dir.mkdir(parents=True, exist_ok=True)

        for prompt_file in list_of_prompt_files:
            output_file = output_dir / f"{prompt_file.stem}.txt"

            if output_file.exists():
                print(f"[SKIP] Output already exists: {output_file.name}")
                continue

            with open(prompt_file, "r", encoding="utf-8") as f:
                prompt_content = f.read()

            token_count = self.count_tokens(prompt_content)
            if token_count > 100_000:
                print(
                    f"[SKIP] {prompt_file.name} "
                    f"(CONTEXT_SIZE={token_count} > 100k)"
                )
                continue

            response = llm_engine.generate(prompt_content)

            with open(output_file, "w", encoding="utf-8") as out_f:
                out_f.write(response)

            print(f"[OK] Saved DeepSeek output to {output_file.name}")

    def detect_qwen(self, list_of_prompt_files):
        llm_config = {
            "model": "qwen/qwen3-coder",
            "max_input_tokens": 100_000,
            "max_output_tokens": 8192,
            "temperature": 0.1
        }

        llm_engine = OpenRouterEngine(**llm_config)

        output_dir = Path(
                os.getenv("OUTPUT_PATH"),
                "llm_outputs",
                self.project_name,
                "hublike_modularization",
                "qwen"
            )
        output_dir.mkdir(parents=True, exist_ok=True)

        for prompt_file in list_of_prompt_files:

            output_file = output_dir / f"{prompt_file.stem}.txt"

            if output_file.exists():
                print(f"Output already exists: {output_file.name}")
                continue

            with open(prompt_file, "r") as f:
                prompt_content = f.read()

            response = llm_engine.generate(prompt_content)

            with open(output_file, "w") as out_f:
                out_f.write(response)