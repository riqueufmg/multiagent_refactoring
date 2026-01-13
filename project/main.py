from pathlib import Path
from dotenv import load_dotenv
from agents.detecting_agent import DetectingAgent
from utils.god_component_comparison import GodComponentComparison
from utils.unstable_dependency import UnstableDependencyComparison
from utils.insufficient_modularization import InsufficientModularizationComparison
from utils.hublike_modularization import HublikeModularizationComparison

def main():

    load_dotenv()

    ## TODO: create a csv file with all projects and loop over it
    projects_list = [
        {
            "project_name": "byte-buddy",
            "classes_path": "data/repositories/byte-buddy/byte-buddy-agent/target;data/repositories/byte-buddy/byte-buddy-android/target;data/repositories/byte-buddy/byte-buddy-android-test/target;data/repositories/byte-buddy/byte-buddy-benchmark/target;data/repositories/byte-buddy/byte-buddy-dep/target;data/repositories/byte-buddy/byte-buddy-gradle-plugin/target;data/repositories/byte-buddy/byte-buddy-maven-plugin/target"
        },
        {
            "project_name": "commons-io",
            "classes_path": "data/repositories/commons-io/target"
        },
        {
            "project_name": "commons-lang",
            "classes_path": "data/repositories/commons-lang/target"
        },
        {
            "project_name": "google-java-format",
            "classes_path": "data/repositories/google-java-format/core/target"
        },
        {
            "project_name": "gson",
            "classes_path": "data/repositories/gson/metrics/target;data/repositories/gson/test-jpms/target;data/repositories/gson/test-graal-native-image/target;data/repositories/gson/gson/target;data/repositories/gson/extras/target;data/repositories/gson/test-shrinker/target;data/repositories/gson/target;data/repositories/gson/proto/target"
        },
        {
            "project_name": "jsoup",
            "classes_path": "data/repositories/jsoup/target/classes"
        },
        {
            "project_name": "javaparser",
            "classes_path": "data/repositories/javaparser/javaparser-core/target;data/repositories/javaparser/javaparser-core-generators/target;data/repositories/javaparser/javaparser-core-metamodel-generator/target;data/repositories/javaparser/javaparser-core-serialization/target;data/repositories/javaparser/javaparser-core-testing/target;data/repositories/javaparser/javaparser-core-testing-bdd/target;data/repositories/javaparser/javaparser-symbol-solver-core/target;data/repositories/javaparser/javaparser-symbol-solver-testing/target;"
        },
        {
            "project_name": "jimfs",
            "classes_path": "data/repositories/jimfs/jimfs/target"
        },
        {
            "project_name": "jitwatch",
            "classes_path": "data/repositories/jitwatch/core/target;data/repositories/jitwatch/ui/target"
        },
        {
            "project_name": "zxing",
            "classes_path": "data/repositories/zxing/target;data/repositories/zxing/core/target;data/repositories/zxing/javase/target"
        },
    ]

    smells_list = [
        #{
        #    "smell_name": "God Component",
        #    "smell_definition": "when a component is **excessively** large either in terms of Lines Of Code or the number of classes.",
        #},
        #{
        #    "smell_name": "Unstable Dependency",
        #    "smell_definition": "This smell occurs when a package depends on other packages that are less stable than itself, violating the Stable Dependencies Principle."
        #},
        #{
        #    "smell_name": "Insufficient Modularization",
        #    "smell_definition": "when a class concentrates an **excessive** number of responsibilities, resulting in a large or complex implementation and an interface that is difficult to understand, use, or evolve.",
        #},
        {
            "smell_name": "Hublike Modularization",
            "smell_definition": "when an abstraction has dependencies (both incoming and outgoing) with a large number of other abstractions.",
        }
    ]

    engines = [
        #"gpt",
        #"deepseek",
        "qwen",
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
            for engine in engines:
                detector.detect(smell["smell_name"], list_of_prompt_files, engine)

        smell_classes_map = {
            "God Component": GodComponentComparison,
            "Unstable Dependency": UnstableDependencyComparison,
            "Insufficient Modularization": InsufficientModularizationComparison,
            "Hublike Modularization": HublikeModularizationComparison,
        }

        for engine in engines:
            for smell in smells_list:
                smell_name = smell["smell_name"]
                SmellClass = smell_classes_map[smell_name]
                consolidator = SmellClass(project_data['project_name'], engine)

                llm_file = consolidator.consolidate_llm_outputs(project_data['project_name'])
                designite_file = consolidator.consolidate_designite_outputs(project_data['project_name'])
                print(f"[{smell_name}][{engine}] Consolidated file created at: {llm_file}")

                base_path = f"data/processed/consolidated_detection/{project_data['project_name']}/{smell_name.lower().replace(' ', '_')}/{engine}"
                llm_file_path = f"{base_path}/{smell_name.lower().replace(' ', '_')}_llm.json"
                designite_file_path = f"{base_path}/{smell_name.lower().replace(' ', '_')}_designite.json"

                metrics_file = consolidator.generate_metrics_file(llm_file_path, designite_file_path)
                print(f"[{smell_name}][{engine}] Metrics file created at: {metrics_file}")

if __name__ == "__main__":
    main()