import json
from pathlib import Path
from agents.llm_inference.llm_engine import LLMInferenceEngine
from agents.llm_inference.gpt_engine import GPTEngine

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

        '''llm_config = {
            "model_name_or_path": "meta-llama/Llama-3.1-8B-Instruct",
            "model_name": "gpt-5mini",
            "max_input_tokens": 2048,
            "max_total_tokens": 4096,
            "temperature": 0.2,
            "top_k": 50,
            "top_p": 0.9
        }'''

        llm_config = {
            "model_name": "gpt-5-mini",
            "max_input_tokens": 10240,
            "max_completion_tokens": 1024
        }

        #llm_engine = LLMInferenceEngine(**llm_config)
        llm_engine = GPTEngine(**llm_config)

        i = 0

        for prompt_file in list_of_prompt_files:

            i += 1

            if i <= 6:
                continue

            with open(prompt_file, "r") as f:
                prompt_content = f.read()

            #llm_engine.load_model()
            #response = llm_engine.generate(prompt_content)

            response = llm_engine.generate(prompt_content)

            output_file = Path("data", "processed", "llm_outputs", self.project_name, f"{prompt_file.stem}.txt")
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, "w") as out_f:
                out_f.write(response)