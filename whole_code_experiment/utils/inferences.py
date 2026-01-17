import json
import os
from pathlib import Path
from utils.gpt_engine import GPTEngine
from utils.deepseek_engine import DeepSeekEngine
from utils.openrouter_engine import OpenRouterEngine

class Inference:

    def __init__(self, smell):
        self.engine = OpenRouterEngine(model="gpt-5-mini")
        self.smell = smell

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
            
            output_dir = Path(
                os.getenv("OUTPUT_PATH"),
                "llm_outputs",
                self.smell,
                "gpt"
            )
            output_dir.mkdir(parents=True, exist_ok=True)

            response = llm_engine.generate(prompt_content)

            output_file = output_dir / f"{prompt_file.stem}.txt"
            
            with open(output_file, "w") as out_f:
                out_f.write(response)
    
    def detect_deepseek(self, list_of_prompt_files):

        llm_config = {
            "model_name": "deepseek-chat",
            "max_input_tokens": 100000,
            "max_completion_tokens": 8192,
        }

        llm_engine = DeepSeekEngine(**llm_config)

        for prompt_file in list_of_prompt_files:

            with open(prompt_file, "r") as f:
                prompt_content = f.read()

            response = llm_engine.generate(prompt_content)

            output_dir = Path(
                os.getenv("OUTPUT_PATH"),
                "llm_outputs",
                self.smell,
                "deepseek"
            )
            output_dir.mkdir(parents=True, exist_ok=True)

            output_file = output_dir / f"{prompt_file.stem}.txt"

            with open(output_file, "w") as out_f:
                out_f.write(response)
    
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
                self.smell,
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