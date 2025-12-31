import subprocess
from pathlib import Path
import shutil
import os

class ProjectCleaner:

    def __init__(self, project_name: str):
        self.project_name = project_name

        self.REPO_DIR = Path(os.getenv("REPO_DIR"))
        self.CLEAN_DIR = Path(os.getenv("CLEAN_DIR"))
        self.JAR_PATH = os.getenv("JAR_PATH")

        if not self.REPO_DIR.exists():
            raise RuntimeError(f"Repository folder {self.REPO_DIR} does not exist")

        self.project_path = self.REPO_DIR / project_name

    def clean_java_file(self, input_path: Path, output_path: Path):

        # Create same folder structure before writing output
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with input_path.open("r", encoding="utf-8") as f:
            content = f.read()

        result = subprocess.run(
            ["java", "-jar", self.JAR_PATH],
            input=content.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        if result.returncode != 0:
            print(f"[ERROR] Failed cleaning {input_path}:\n{result.stderr.decode()}")
            return

        with output_path.open("w", encoding="utf-8") as f:
            f.write(result.stdout.decode())

    def clean_repo(self):
        print(f"\nCleaning repository: {self.project_name}")

        if not self.project_path.exists():
            print(f"Warning: repository {self.project_path} does not exist, skipping")
            return

        # Base output root
        repo_output_root = self.CLEAN_DIR / self.project_name

        for java_file in self.project_path.rglob("*.java"):
            relative_path = java_file.relative_to(self.project_path)
            output_path = repo_output_root / relative_path

            self.clean_java_file(java_file, output_path)

        print(f"Finished cleaning: {self.project_name}")

    def get_cleaned_file(self, original_path: Path) -> str | None:

        # Ensure it's a Path object
        original_path = Path(original_path)

        # Convert input path into relative path inside the project
        try:
            relative_path = original_path.relative_to(self.project_path)
        except ValueError:
            # User may have passed an absolute path, e.g., data/repositories/google-java-format/...
            # Try making it relative manually
            if str(original_path).startswith(str(self.project_path)):
                relative_path = Path(str(original_path).replace(str(self.project_path), "").lstrip("/"))
            else:
                raise RuntimeError(
                    f"Provided path does not belong to this repository: {original_path}"
                )

        # Cleaned file path
        cleaned_file_path = self.CLEAN_DIR / self.project_name / relative_path

        if not cleaned_file_path.exists():
            print(f"[WARN] Cleaned java file not found: {cleaned_file_path}")
            return None

        return cleaned_file_path.read_text(encoding="utf-8")