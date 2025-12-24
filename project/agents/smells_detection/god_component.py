import json
from pathlib import Path
import os

from agents.llm_inference.llm_engine import LLMInferenceEngine
from agents.llm_inference.gpt_engine import GPTEngine

class GodComponentDetector:

    def __init__(self, project_name):
        self.project_name = project_name
        self.json_path = f"{os.getenv("OUTPUT_PATH")}/metrics/{project_name}/project_metrics.json"
        self.prompts_path = os.getenv("PROMPTS_PATH")

    def filter_data(self):
        if not Path(self.json_path).exists():
            raise FileNotFoundError(f"JSON file not found: {self.json_path}")

        with open(self.json_path, "r") as f:
            data = json.load(f)

        return data.get("packages", [])
    
    def generate_prompts(self, smell):
        packages = self.filter_data()

        with open(Path(self.prompts_path, "templates", "detection_god_component.tpl"), "r") as file:
            template_content = file.read()
        
        list_of_prompt_files = []

        for package in packages:

            ## TODO: remove it later, because I've defined one template per smell
            prompt = template_content.replace("{SMELL_NAME}", smell['smell_name']) \
                         .replace("{SMELL_DEFINITION}", smell['smell_definition']) \
                         .replace("{INPUT_DATA}", json.dumps(package))
            
            Path(
                self.prompts_path,
                "generated",
                "smell_detection",
                f"{smell['smell_name'].replace(' ', '').lower()}",
                self.project_name
            ).mkdir(parents=True, exist_ok=True)

            prompt_file = Path(
                self.prompts_path,
                "generated",
                "smell_detection",
                f"{smell['smell_name'].replace(' ', '').lower()}",
                self.project_name,
                f"{package['package'].replace('/', '_')}.txt"
            )

            with open(prompt_file, "w") as f:
                f.write(prompt)
                list_of_prompt_files.append(prompt_file)
        
        return list_of_prompt_files
    
    def detect_gpt(self, list_of_prompt_files):

        llm_config = {
            "model_name": "gpt-5-mini",
            "max_input_tokens": 10240,
            "max_completion_tokens": 4096,
        }

        llm_engine = GPTEngine(**llm_config)

        for prompt_file in list_of_prompt_files:

            with open(prompt_file, "r") as f:
                prompt_content = f.read()

            response = llm_engine.generate(prompt_content)

            output_file = Path("data", "processed", "llm_outputs", self.project_name, "god_component", f"{prompt_file.stem}.txt")
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, "w") as out_f:
                out_f.write(response)
        
    def detect_hf(self, list_of_prompt_files):

        llm_config = {
            "model_name_or_path": "meta-llama/Llama-3.2-3B-Instruct",
            "max_input_tokens": 2048,
            "max_total_tokens": 4096,
            "temperature": 0.2,
            "top_k": 50,
            "top_p": 0.9
        }

        llm_engine = LLMInferenceEngine(**llm_config)

        for prompt_file in list_of_prompt_files:

            with open(prompt_file, "r") as f:
                prompt_content = f.read()

            llm_engine.load_model()
            response = llm_engine.generate(prompt_content)

            output_file = Path("data", "processed", "llm_outputs", self.project_name, "god_component", f"{prompt_file.stem}.txt")
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, "w") as out_f:
                out_f.write(response)