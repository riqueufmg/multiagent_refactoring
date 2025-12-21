import json
from pathlib import Path
from agents.llm_inference.llm_engine import LLMInferenceEngine

class GodComponentDetector:

    def __init__(self, project_name, json_path, prompts_path):
        self.project_name = project_name
        self.json_path = Path(json_path)
        self.prompts_path = Path(prompts_path)

    def load_packages(self):
        if not self.json_path.exists():
            raise FileNotFoundError(f"JSON file not found: {self.json_path}")

        with open(self.json_path, "r") as f:
            data = json.load(f)

        return data.get("packages", [])
    
    def generate_prompts(self, smell):
        packages = self.load_packages()

        with open(Path(self.prompts_path, "templates", "smells_detection.tpl"), "r") as file:
            template_content = file.read()
        
        list_of_prompt_files = []

        for package in packages:

            prompt = template_content.replace("{SMELL_NAME}", smell['name']) \
                         .replace("{SMELL_DEFINITION}", smell['definition']) \
                         .replace("{INPUT_DATA}", json.dumps(package))
            
            Path(
                self.prompts_path,
                "generated",
                "smell_detection",
                f"{smell['name'].replace(' ', '').lower()}",
                self.project_name
            ).mkdir(parents=True, exist_ok=True)

            prompt_file = Path(
                self.prompts_path,
                "generated",
                "smell_detection",
                f"{smell['name'].replace(' ', '').lower()}",
                self.project_name,
                f"{package['package'].replace('/', '_')}.txt"
            )

            with open(prompt_file, "w") as f:
                f.write(prompt)
                list_of_prompt_files.append(prompt_file)
        
        return list_of_prompt_files
    
    def detect(self, smell):
        list_of_prompt_files = self.generate_prompts(smell)

        llm_config = {
            "model_name_or_path": "meta-llama/Llama-3.2-1B",
            "max_input_tokens": 2048,
            "max_total_tokens": 4096,
            "temperature": 0.7,
            "top_k": 50,
            "top_p": 0.9
        }

        llm_engine = LLMInferenceEngine(**llm_config)
        llm_engine.infer("")