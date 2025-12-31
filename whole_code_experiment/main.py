import subprocess
from pathlib import Path
import shutil

# Caminhos
REPO_DIR = Path("data/repositories")
CLEAN_DIR = Path("data/clean_repos")
JAR_PATH = Path("tools/java-cleaner/target/java-cleaner-0.1.0-jar-with-dependencies.jar")

# Limpar diretório clean_repos se já existir
if CLEAN_DIR.exists():
    shutil.rmtree(CLEAN_DIR)
CLEAN_DIR.mkdir(parents=True, exist_ok=True)

def clean_java_file(input_path: Path, output_path: Path):
    """
    Chama o cleaner.jar para limpar o arquivo .java
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with input_path.open("r", encoding="utf-8") as f:
        content = f.read()

    result = subprocess.run(
        ["java", "-jar", str(JAR_PATH)],
        input=content.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    if result.returncode != 0:
        print(f"Erro ao processar {input_path}:\n{result.stderr.decode()}")
        return

    with output_path.open("w", encoding="utf-8") as f:
        f.write(result.stdout.decode())

def process_all_repos():
    """
    Processa todos os repositórios e gera mirror limpo
    """
    for repo_path in REPO_DIR.iterdir():
        if not repo_path.is_dir():
            continue

        for java_file in repo_path.rglob("*.java"):
            # Determinar package para manter estrutura
            package_parts = []
            with java_file.open("r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("package "):
                        package_name = line.split()[1].rstrip(";")
                        package_parts = package_name.split(".")
                        break

            class_name = java_file.stem
            output_path = CLEAN_DIR / repo_path.name / "src" / "main" / "java" / Path(*package_parts) / f"{class_name}.java"
            clean_java_file(java_file, output_path)

    print("Processamento de todos os repositórios concluído!")

def get_clean_file(package: str, classname: str, project: str) -> Path:
    """
    Retorna o Path do arquivo limpo a partir de package + classe + projeto
    """
    path = CLEAN_DIR / project / "src" / "main" / "java" / Path(*package.split(".")) / f"{classname}.java"
    if path.exists():
        return path
    else:
        raise FileNotFoundError(f"{package}.{classname} não encontrado no projeto {project}")

if __name__ == "__main__":
    process_all_repos()
    # Exemplo de recuperação
    # path = get_clean_file("com.example", "A", "project1")
    # print(path)