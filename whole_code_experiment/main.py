from dotenv import load_dotenv
from pathlib import Path
from utils.clean_projects import ProjectCleaner
from utils.openrouter_engine import OpenRouterEngine
from smells_detection.god_component import GodComponentDetector
from smells_detection.hublike_modularization import HublikeModularizationDetector
from smells_detection.insufficient_modularization import InsufficientModularizationDetector
from smells_detection.unstable_dependency import UnstableDependencyDetector

import csv

def save_context_sizes_csv(prompt_files: list[Path], output_path: Path, max_context_size: int):
    rows = []
    for pf in prompt_files:
        with open(pf, "r", encoding="utf-8") as f:
            first_line = f.readline().strip()
            if first_line.startswith("##CONTEXT_SIZE="):
                try:
                    context_size = int(first_line.replace("##CONTEXT_SIZE=", ""))
                except ValueError:
                    context_size = -1
            else:
                context_size = -1

        if context_size <= max_context_size:
            rows.append({
                "prompt_file": str(pf),
                "context_size": context_size
            })

    output_csv = output_path / "candidates.csv"
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["prompt_file", "context_size", "is_large"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    print(f"Saved context sizes CSV: {output_csv}")

def merge_all_candidates(projects_list: list[str]):
    """
    Agrupa todos os candidatos (candidates.csv) de todos os projetos
    em um único CSV por smell e salva em data/processed/candidates/
    """
    smells = {
        "God Component": Path("data/processed/prompts/god_component"),
        "Unstable Dependency": Path("data/processed/prompts/unstable_dependency"),
        "Insufficient Modularization": Path("data/processed/prompts/insufficient_modularization"),
        "Hublike Modularization": Path("data/processed/prompts/hublike_modularization"),
    }

    output_dir = Path("data/processed/candidates")
    output_dir.mkdir(parents=True, exist_ok=True)

    for smell_name, base_path in smells.items():
        merged_rows = []

        for project in projects_list:
            candidates_csv = base_path / project / "candidates.csv"
            if not candidates_csv.exists():
                continue

            with open(candidates_csv, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    merged_rows.append({
                        "project": project,
                        "smell": smell_name,
                        "prompt_file": row["prompt_file"],
                        "context_size": row["context_size"],
                        "is_large": row.get("is_large", "")
                    })

        if not merged_rows:
            print(f"[WARN] No candidates found for smell {smell_name}")
            continue

        output_csv = output_dir / f"{smell_name.replace(' ', '_').lower()}.csv"
        with open(output_csv, "w", newline="", encoding="utf-8") as f:
            fieldnames = ["project", "smell", "prompt_file", "context_size", "is_large"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(merged_rows)

        print(f"[OK] Merged candidates saved: {output_csv}")

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

            #list_of_prompt_files = detector.generate_prompts()
            #print(f"Generated {len(list_of_prompt_files)} prompts for project {project}")

            max_context_size = 100_000

            list_of_prompt_files = sorted(output_path.glob("*.txt"))
            save_context_sizes_csv(list_of_prompt_files, output_path, max_context_size)
    
    ## 3. Generate the candidates
    merge_all_candidates(projects_list)

if __name__ == "__main__":
    main()