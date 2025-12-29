import subprocess
from pathlib import Path

class DesigniteRunner:

    def __init__(self, project_path, output_path, classes_path):
        self.project_path = project_path
        self.output_path = output_path
        self.classes_path = classes_path

    def run(self):
        Path(self.output_path).mkdir(parents=True, exist_ok=True)
        cmd = [
            "java", "-jar", "tools/DesigniteJava2.8.3.jar",
            "-i", self.project_path,
            "-o", self.output_path,
            #"-c", self.classes_path,
            "-g",
        ]
        subprocess.run(cmd, capture_output=True, text=True)
        print(f"Designite execution completed. Output at {self.output_path}")