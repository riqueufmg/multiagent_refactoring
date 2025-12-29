from agents.detecting_agent import DetectingAgent
from agents.smells_detection.god_component import GodComponentDetector
from pathlib import Path
from dotenv import load_dotenv

def main():

    load_dotenv()

    ## TODO: create a csv file with all projects and loop over it

    projects_list = [
        #{
        #    "project_name": "jsoup",
        #    "classes_path": "data/repositories/jsoup/target/classes"
        #},
        #{
        #    "project_name": "zxing",
        #    "classes_path": "data/repositories/zxing/target;data/repositories/zxing/core/target;data/repositories/zxing/javase/target"
        #},
        #{
        #    "project_name": "byte-buddy",
        #    "classes_path": "data/repositories/byte-buddy/byte-buddy-agent/target;data/repositories/byte-buddy/byte-buddy-android/target;data/repositories/byte-buddy/byte-buddy-android-test/target;data/repositories/byte-buddy/byte-buddy-benchmark/target;data/repositories/byte-buddy/byte-buddy-dep/target;data/repositories/byte-buddy/byte-buddy-gradle-plugin/target;data/repositories/byte-buddy/byte-buddy-maven-plugin/target"
        #},
        #{
        #    "project_name": "google-java-format",
        #    "classes_path": "data/repositories/google-java-format/core/target"
        #},
        #{
        #    "project_name": "jimfs",
        #    "classes_path": "data/repositories/jimfs/jimfs/target"
        #},
        {
            "project_name": "jitwatch",
            "classes_path": "data/repositories/jitwatch/core/target;data/repositories/jitwatch/ui/target"
        },
    ]

    smells_list = [
        {
            "smell_name": "God Component",
            "smell_definition": "when a component is **excessively** large either in terms of Lines Of Code or the number of classes.",
        },
        {
            "smell_name": "Insufficient Modularization",
            "smell_definition": "when a class concentrates an **excessive** number of responsibilities, resulting in a large or complex implementation and an interface that is difficult to understand, use, or evolve.",
        },
        {
            "smell_name": "Unstable Dependency",
            "smell_definition": "This smell occurs when a package depends on other packages that are less stable than itself, violating the Stable Dependencies Principle."
        },
    ]
    
    ## Loop over projects
    for project_data in projects_list:

        ## 1. Create the Detecting Agent ##
        detector = DetectingAgent(**project_data)

        ## 2. Generate the input metrics JSON file
        metrics_json = detector.collect_metrics()

        ## Loop over smells
        for smell in smells_list:
            # 3. Generate Prompts
            list_of_prompt_files = detector.generate_prompts(**smell)

            # 4. Detect Smells
            detector.detect(smell["smell_name"], list_of_prompt_files)

if __name__ == "__main__":
    main()