import csv
from pathlib import Path
from collections import Counter

metrics_dir = Path(".")

smell_counter = Counter()

# Itera pelos diretórios de projetos
for project_dir in metrics_dir.iterdir():
    if project_dir.is_dir():
        # Lista de arquivos de smells
        smell_files = ["DesignSmells.csv", "ArchitectureSmells.csv"]
        for smell_file in smell_files:
            csv_file = project_dir / smell_file
            if csv_file.exists():
                with open(csv_file, newline="", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        smell_name = row["Smell"].strip()
                        smell_counter[smell_name] += 1

# Salva a contagem total em um CSV
output_file = metrics_dir / "smells_count.csv"
with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["smell_name", "count"])
    for smell, count in smell_counter.most_common():
        writer.writerow([smell, count])

print(f"File saved on {output_file}")
