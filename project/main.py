from agents.detecting_agent import DetectingAgent
from agents.smells_detection.god_component import GodComponentDetector
from pathlib import Path
from dotenv import load_dotenv

def main():

    load_dotenv()

    ## TODO: create a csv file with all projects and loop over it
    project_data = {
        "project_name": "jsoup",
        "classes_path": "data/repositories/jsoup/target/classes",
        "jar_path": "data/repositories/jsoup/target/jsoup-1.22.1-SNAPSHOT.jar"
    }
    
    ## 1. Create the Detecting Agent ##
    detector = DetectingAgent(**project_data)

    ## 2. Generate the input metrics JSON file
    metrics_json = detector.collect_metrics()

    ## 3. Generate prompts ##
    smell = {
        "smell_name": "God Component",
        "smell_definition": "when a component is **excessively** large either in terms of Lines Of Code or the number of classes."
    }

    list_of_prompt_files = detector.generate_prompts(**smell)

    ## 4. Detect using GPT ##
    detector.detect(smell["smell_name"], list_of_prompt_files)

if __name__ == "__main__":
    main()