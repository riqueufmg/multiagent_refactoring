import re
from pathlib import Path

class Fqn:
    PACKAGE_RE = re.compile(
        r'^\s*package\s+([a-zA-Z_]\w*(?:\.[a-zA-Z_]\w*)*)\s*;',
        re.MULTILINE
    )
    TYPE_RE = re.compile(
        r'\b(class|interface|enum|record)\s+([A-Za-z_]\w*)'
    )

    IGNORED_DIRS = {
        ".git", "build", "target", ".gradle",
        "node_modules", "__pycache__",
        "test", "tests"
    }

    def __init__(self, fqn: str):
        self.fqn = fqn.strip()
    
    def exists_in_repo(self, repo_path: str) -> bool:
        return self.find_in_repo(repo_path) is not None

    def _read(self, path: Path) -> str | None:
        for enc in ("utf-8", "latin-1"):
            try:
                return path.read_text(encoding=enc)
            except:
                pass
        return None

    def _extract_package(self, text: str) -> str | None:
        match = self.PACKAGE_RE.search(text)
        return match.group(1) if match else None

    def _has_type(self, text: str, type_name: str) -> bool:
        return any(m.group(2) == type_name for m in self.TYPE_RE.finditer(text))

    def find_in_repo(self, repo_path: str) -> Path | None:
        repo = Path(repo_path)

        if not repo.is_dir() or not self.fqn:
            return None

        pkg, _, cls = self.fqn.rpartition(".")
        wants_type = bool(pkg and cls)

        for path in repo.rglob("*.java"):
            if any(p in self.IGNORED_DIRS for p in path.parts):
                continue

            text = self._read(path)
            if not text:
                continue

            package_name = self._extract_package(text)

            if package_name == self.fqn:
                return path.parent  # diretório do pacote

            if wants_type and package_name == pkg:
                if self._has_type(text, cls):
                    return path  # arquivo da classe

        return None
    
    def _java_file_to_fqn(self, rel_path: str, source_root: str) -> str:
        p = Path(rel_path).with_suffix("")
        root = Path(source_root)

        rel = p.relative_to(root)
        return ".".join(rel.parts)

    def _java_files_to_fqns(self, rel_paths: list[str], source_root: str) -> set[str]:
        return {
            self._java_file_to_fqn(p, source_root)
            for p in rel_paths
            if p.endswith(".java") and not p.endswith("package-info.java")
        }

# How to use:

#fqn = Fqn("data/repositories/jsoup")

# path = fqn.find_in_repo("org.foo.bar.Classe")
# print(path) >> /repo/.../Classe.java

#path = fqn.find_in_repo("org.jsoup.nodes")
#print(path) #>> /repo/.../org/foo/bar/