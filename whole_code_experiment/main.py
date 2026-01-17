import csv
from dotenv import load_dotenv
from pathlib import Path
from utils.filter_prompts import FilterPrompts
from utils.inferences import Inference
from smells_detection.god_component import GodComponentDetector
from smells_detection.hublike_modularization import HublikeModularizationDetector
from smells_detection.insufficient_modularization import InsufficientModularizationDetector
from smells_detection.unstable_dependency import UnstableDependencyDetector

def main():
    load_dotenv()

    projects_list = [
        "byte-buddy",
        "commons-io",
        "commons-lang",
        "google-java-format",
        "gson",
        "javaparser",
        "jimfs",
        "jitwatch",
        "jsoup",
        "zxing",
    ]

    smell_list = [
        "God Component",
        "Unstable Dependency",
        "Insufficient Modularization",
        "Hublike Modularization"
    ]

    ## Project by project
    for project in projects_list:

        for smell in smell_list:

            ## 1. Generate prompts
            if smell == "God Component":
                detector = GodComponentDetector(project)
                output_path = Path(f"data/processed/prompts/god_component/{project}")
            elif smell == "Unstable Dependency":
                detector = UnstableDependencyDetector(project)
                output_path = Path(f"data/processed/prompts/unstable_dependency/{project}")
            elif smell == "Insufficient Modularization":
                detector = InsufficientModularizationDetector(project)
                output_path = Path(f"data/processed/prompts/insufficient_modularization/{project}")
            elif smell == "Hublike Modularization":
                detector = HublikeModularizationDetector(project)
                output_path = Path(f"data/processed/prompts/hublike_modularization/{project}")

            ## TODO: Remove comments after the inferences
            #list_of_prompt_files = detector.generate_prompts()
            #print(f"Generated {len(list_of_prompt_files)} prompts for project {project}")

            max_context_size = 100_000
            list_of_prompt_files = sorted(output_path.glob("*.txt"))

            ## TODO: Remove comments after the inferences
            #filter = FilterPrompts(max_context_size)
            #filter.save_context_sizes_csv(list_of_prompt_files, output_path)
    
    ## 3. Generate the candidates
    ## TODO: Remove comments after the inferences
    #filter.merge_all_candidates(projects_list)

    ## 4. Select samples
    ## TODO: Remove comments after the inferences
    '''candidates_dir = Path("data/processed/candidates")
    sample_dir = Path("data/processed/candidates_sampled")
    sample_dir.mkdir(parents=True, exist_ok=True)

    for smell_name in smell_list:
        input_csv = candidates_dir / f"{smell_name.replace(' ', '_').lower()}.csv"
        output_csv = sample_dir / f"{smell_name.replace(' ', '_').lower()}_sample.csv"

        if smell_name == "God Component" or smell_name == "Unstable Dependency":
            sample_size = 183
        else:
            sample_size = 360

        filter.sample_candidates(
            candidates_csv=input_csv,
            sample_csv=output_csv,
            sample_size=sample_size,
            ratio_positive=0.1
        )'''

    # 5. Detect Smells

    ## 5.1 God Component
    candidates_csv = Path("data/processed/candidates_sampled/god_component_sample.csv")

    list_of_prompt_files = []
    with open(candidates_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            prompt_path = Path(row["prompt_file"])
            if prompt_path.exists():
                list_of_prompt_files.append(prompt_path)

    print(f"Loaded {len(list_of_prompt_files)} prompt files for God Component.")

    inference = Inference("god_component")
    #inference.detect_gpt(list_of_prompt_files)
    #inference.detect_qwen(list_of_prompt_files)
    inference.detect_deepseek(list_of_prompt_files)

    # 5.2 Unstable Dependency
    candidates_csv = Path("data/processed/candidates_sampled/unstable_dependency_sample.csv")

    list_of_prompt_files = []
    with open(candidates_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            prompt_path = Path(row["prompt_file"])
            if prompt_path.exists():
                list_of_prompt_files.append(prompt_path)

    print(f"Loaded {len(list_of_prompt_files)} prompt files for Unstable Dependency.")

    inference = Inference("unstable_dependency")
    #inference.detect_gpt(list_of_prompt_files)
    #inference.detect_qwen(list_of_prompt_files)
    inference.detect_deepseek(list_of_prompt_files)

    # 5.3 Insufficient Modularization
    candidates_csv = Path("data/processed/candidates_sampled/insufficient_modularization_sample.csv")

    list_of_prompt_files = []
    with open(candidates_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            prompt_path = Path(row["prompt_file"])
            if prompt_path.exists():
                list_of_prompt_files.append(prompt_path)

    print(f"Loaded {len(list_of_prompt_files)} prompt files for Insufficient Modularization.")

    inference = Inference("insufficient_modularization")
    #inference.detect_gpt(list_of_prompt_files)
    #inference.detect_qwen(list_of_prompt_files)
    inference.detect_deepseek(list_of_prompt_files)

    # 5.4 Hub-like Modularization
    candidates_csv = Path("data/processed/candidates_sampled/hublike_modularization_sample.csv")

    list_of_prompt_files = []
    with open(candidates_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            prompt_path = Path(row["prompt_file"])
            if prompt_path.exists():
                list_of_prompt_files.append(prompt_path)

    print(f"Loaded {len(list_of_prompt_files)} prompt files for Hublike Modularization.")

    inference = Inference("hublike_modularization")
    #inference.detect_gpt(list_of_prompt_files)
    #inference.detect_qwen(list_of_prompt_files)
    inference.detect_deepseek(list_of_prompt_files)

if __name__ == "__main__":
    main()