from dotenv import load_dotenv
from pathlib import Path
from utils.clean_projects import ProjectCleaner
from utils.openrouter_engine import OpenRouterEngine

def main():
    load_dotenv()

    projects_list = [
        {"project_name": "jsoup"},
        {"project_name": "zxing"},
        {"project_name": "byte-buddy"},
        {"project_name": "google-java-format"},
        {"project_name": "jimfs"},
        {"project_name": "jitwatch"},
    ]

    for project in projects_list:
        break ## TODO: remove break after testing
        cleaner = ProjectCleaner(project["project_name"])
        cleaner.clean_repo()
        print(f"Cleaned file path: {cleaned_file}")
    
    cleaner = ProjectCleaner("google-java-format")
    code = cleaner.get_cleaned_file(
        Path("data/repositories/google-java-format/eclipse_plugin/src/com/google/googlejavaformat/java/JavaFormatterBase.java")
    )

    engine = OpenRouterEngine(
        model="meta-llama/llama-3.3-70b-instruct:free",
        max_input_tokens=50_000,
        max_output_tokens=2000
    )

    prompt = (
        "Does this class have Insufficiency Modularization smell?\n\n"
        "```java\n"
        f"{code}\n"
        "```\n\n"
        "Provide the output in this structure:\n\n"
        "```json\n"
        "{\n"
        '    "class": "[class name]",\n'
        '    "detection": true,\n'
        '    "justification": "[Key elements that justify why this class suffers from insufficient modularization]"\n'
        "}\n"
        "```\n"
    )

    print("tokens:", engine.count_tokens(prompt))

    result = engine.generate(prompt)
    print(result)
    

if __name__ == "__main__":
    main()