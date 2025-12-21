from agents.detecting_agent import DetectingAgent
from agents.smells_detection.god_component import GodComponentDetector
from pathlib import Path

def main():
    project_name = "jsoup"
    project_path = f"data/repositories/{project_name}"
    output_path = f"data/processed/metrics/{project_name}"
    prompts_path = f"agents/prompts"
    classes_path = f"data/repositories/{project_name}/target/classes"
    jar_path = Path(f"data/repositories/{project_name}/target/jsoup-1.22.1-SNAPSHOT.jar")
    
    detector = DetectingAgent(project_path, output_path, classes_path, jar_path)

    metrics_json = detector.collect_metrics()
    print("Metrics collected!")

    smell = {
        "name": "God Component",
        "definition": "when a component is **excessively** large either in terms of Lines Of Code or the number of classes."
    }

    GodComponentDetector(
        project_name,
        Path(output_path,"project_metrics.json"),
        Path(prompts_path)
    ).detect(smell)

if __name__ == "__main__":
    main()
