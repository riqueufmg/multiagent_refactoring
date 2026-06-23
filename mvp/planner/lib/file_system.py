from pathlib import Path

class FileSystem:
    def __init__(self, repo_path: str, file_path: str):
        self.repo_path = Path(repo_path)
        self.path = Path(file_path)

    ## return Java files from a package
    def list_java_files_in_dir(self) -> list[str]:
        if not self.path.exists() or not self.path.is_dir():
            return []

        java_files = []
        
        for f in sorted(self.path.glob("*.java")):
            relative = f.relative_to(self.repo_path)
            java_files.append(str(relative))
        
        return java_files

# How to use:
#fs = FileSystem("data/repositories/jsoup", "data/repositories/jsoup/src/main/java/org/jsoup/nodes")

#for i in fs.list_java_files_in_dir():
#    print(i)