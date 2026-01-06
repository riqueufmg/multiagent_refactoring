import json
from pathlib import Path
import os

from agents.llm_inference.llm_engine import LLMInferenceEngine
from agents.llm_inference.gpt_engine import GPTEngine

class GodComponentDetector:

    def __init__(self, project_name):
        self.project_name = project_name
        self.json_path = f"{os.getenv('OUTPUT_PATH')}/metrics/{project_name}/project_metrics.json"
        self.prompts_path = os.getenv("PROMPTS_PATH")

    def filter_data(self):
        if not Path(self.json_path).exists():
            raise FileNotFoundError(f"JSON file not found: {self.json_path}")

        with open(self.json_path, "r") as f:
            data = json.load(f)

        return data.get("packages", [])

    def generate_prompts(self, smell):
        packages = self.filter_data()

        with open(
            Path(self.prompts_path, "templates", "detection_god_component.tpl"),
            "r"
        ) as file:
            template_content = file.read()

        list_of_prompt_files = []

        output_dir = Path(
            os.getenv("OUTPUT_PATH"),
            "prompts",
            "smell_detection",
            "god_component",
            self.project_name
        )
        output_dir.mkdir(parents=True, exist_ok=True)

        for package in packages:
            prompt_content = (
                template_content
                .replace("{SMELL_NAME}", smell["smell_name"])
                .replace("{SMELL_DEFINITION}", smell["smell_definition"])
                .replace("{INPUT_DATA}", json.dumps(package))
            )

            pkg_filename = package["package"].replace("/", "_")
            prompt_file = output_dir / f"{pkg_filename}.txt"

            with open(prompt_file, "w") as f:
                f.write(prompt_content)

            list_of_prompt_files.append(prompt_file)

        return list_of_prompt_files

    def detect_gpt(self, list_of_prompt_files):

        llm_config = {
            "model_name": "gpt-5-mini",
            "max_input_tokens": 100000,
            "max_completion_tokens": 30720,
        }

        llm_engine = GPTEngine(**llm_config)

        for prompt_file in list_of_prompt_files:

            with open(prompt_file, "r") as f:
                prompt_content = f.read()

            response = llm_engine.generate(prompt_content)

            output_dir = Path(os.getenv("OUTPUT_PATH"), "llm_outputs", self.project_name, "god_component")
            output_dir.mkdir(parents=True, exist_ok=True)
            output_file = output_dir / f"{prompt_file.stem}.txt"
            with open(output_file, "w") as out_f:
                out_f.write(response)