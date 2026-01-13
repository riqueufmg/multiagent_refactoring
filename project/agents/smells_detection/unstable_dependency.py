import json
from pathlib import Path
import os

from agents.llm_inference.gpt_engine import GPTEngine
from agents.llm_inference.deepseek_engine import DeepSeekEngine
from agents.llm_inference.openrouter_engine import OpenRouterEngine

class UnstableDependencyDetector:

    def __init__(self, project_name):
        self.project_name = project_name
        self.json_path = f"{os.getenv("OUTPUT_PATH")}/metrics/{project_name}/project_metrics.json"
        self.prompts_path = os.getenv("PROMPTS_PATH")

    '''def filter_data(self):
        if not Path(self.json_path).exists():
            raise FileNotFoundError(f"JSON file not found: {self.json_path}")

        with open(self.json_path, "r") as f:
            data = json.load(f)

        return {
            "project": data.get("project"),
            "packages": [
                {
                    "package": p["package"],
                    "metrics": p["metrics"],
                    "dependencies": p.get("dependencies", [])
                }
                for p in data.get("packages", [])
            ]
        }
    '''

    def filter_data(self):
        if not Path(self.json_path).exists():
            raise FileNotFoundError(f"JSON file not found: {self.json_path}")

        with open(self.json_path, "r") as f:
            data = json.load(f)

        packages_index = {pkg["package"]: pkg for pkg in data.get("packages", [])}

        outgoing_map = {}
        for pkg_name, pkg in packages_index.items():
            outgoing = set(pkg.get("dependencies", []))
            outgoing_map[pkg_name] = list(outgoing)

        incoming_map = {pkg_name: [] for pkg_name in packages_index}
        for src, targets in outgoing_map.items():
            for target in targets:
                if target in incoming_map:
                    incoming_map[target].append(src)

        filtered_packages = []
        for pkg_name, pkg in packages_index.items():
            filtered_packages.append({
                "analyzed_package": {
                    "package": pkg_name,
                    "metrics": pkg.get("metrics", {}),
                    "dependencies": outgoing_map.get(pkg_name, [])
                },
                "outgoing_dependencies": [
                    {
                        "package": t,
                        "metrics": packages_index[t]["metrics"],
                        "dependencies": outgoing_map.get(t, [])
                    }
                    for t in outgoing_map.get(pkg_name, [])
                    if t in packages_index
                ],
                "incoming_dependencies": [
                    {
                        "package": t,
                        "metrics": packages_index[t]["metrics"],
                        "dependencies": outgoing_map.get(t, [])
                    }
                    for t in incoming_map.get(pkg_name, [])
                    if t in packages_index
                ]
            })

        return filtered_packages
    
    '''def generate_prompts(self, smell):

        input_data = self.filter_data()

        with open(
            Path(self.prompts_path, "templates", "detection_unstable_dependency.tpl"),
            "r"
        ) as file:
            template_content = file.read()

        prompt = (
            template_content
            .replace("{SMELL_NAME}", smell["smell_name"])
            .replace("{SMELL_DEFINITION}", smell["smell_definition"])
            .replace("{INPUT_DATA}", json.dumps(input_data))
        )

        output_dir = Path(
            self.prompts_path,
            "generated",
            "smell_detection",
            smell["smell_name"].replace(" ", "").lower(),
            self.project_name
        )

        output_dir = Path(
            os.getenv("OUTPUT_PATH"),
            "prompts",
            "smell_detection",
            "unstable_dependency",
            self.project_name
        )
        output_dir.mkdir(parents=True, exist_ok=True)

        prompt_file = output_dir / "unstable_dependency.txt"

        with open(prompt_file, "w") as f:
            f.write(prompt)

        return [prompt_file]
    '''

    def generate_prompts(self, smell):
        input_data = self.filter_data()

        with open(
            Path(self.prompts_path, "templates", "detection_unstable_dependency.tpl"),
            "r"
        ) as file:
            template_content = file.read()

        list_of_prompt_files = []

        for pkg_item in input_data:
            prompt_content = (
                template_content
                .replace("{SMELL_NAME}", smell["smell_name"])
                .replace("{SMELL_DEFINITION}", smell["smell_definition"])
                .replace("{INPUT_DATA}", json.dumps(pkg_item))
            )

            output_dir = Path(
                os.getenv("OUTPUT_PATH"),
                "prompts",
                "smell_detection",
                "unstable_dependency",
                self.project_name
            )
            output_dir.mkdir(parents=True, exist_ok=True)

            pkg_filename = pkg_item["analyzed_package"]["package"].replace("/", "_")
            prompt_file = output_dir / f"{pkg_filename}.txt"

            with open(prompt_file, "w") as f:
                f.write(prompt_content)

            list_of_prompt_files.append(prompt_file)

        return list_of_prompt_files
    
    def detect_gpt(self, list_of_prompt_files):

        llm_config = {
            "model_name": "gpt-5-mini",
            "max_input_tokens": 100000,
            "max_completion_tokens": 30720
        }

        llm_engine = GPTEngine(**llm_config)

        for prompt_file in list_of_prompt_files:

            with open(prompt_file, "r") as f:
                prompt_content = f.read()

            response = llm_engine.generate(prompt_content)

            output_dir = Path(
                os.getenv("OUTPUT_PATH"),
                "llm_outputs",
                self.project_name,
                "unstable_dependency",
                "gpt"
            )
            output_dir.mkdir(parents=True, exist_ok=True)

            output_file = output_dir / f"{prompt_file.stem}.txt"
            
            with open(output_file, "w") as out_f:
                out_f.write(response)
    
    def detect_deepseek(self, list_of_prompt_files):

        llm_config = {
            "model_name": "deepseek-chat",
            "max_input_tokens": 100000,
            "max_completion_tokens": 8192
        }

        llm_engine = DeepSeekEngine(**llm_config)

        for prompt_file in list_of_prompt_files:

            with open(prompt_file, "r") as f:
                prompt_content = f.read()

            response = llm_engine.generate(prompt_content)

            output_dir = Path(
                os.getenv("OUTPUT_PATH"),
                "llm_outputs",
                self.project_name,
                "unstable_dependency",
                "deepseek"
            )
            output_dir.mkdir(parents=True, exist_ok=True)

            output_file = output_dir / f"{prompt_file.stem}.txt"

            with open(output_file, "w") as out_f:
                out_f.write(response)
    
    def detect_qwen(self, list_of_prompt_files):
        llm_config = {
            "model": "qwen/qwen3-coder",
            "max_input_tokens": 100000,
            "max_output_tokens": 8192,
            "temperature": 0.1
        }

        llm_engine = OpenRouterEngine(**llm_config)

        output_dir = Path(
                os.getenv("OUTPUT_PATH"),
                "llm_outputs",
                self.project_name,
                "unstable_dependency",
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