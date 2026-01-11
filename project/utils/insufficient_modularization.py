import json
import csv
import re
from pathlib import Path

class InsufficientModularizationComparison:
    def __init__(self, project_name, engine, base_path="data/processed/"):
        self.project_name = project_name
        self.engine = engine
        self.base_path = Path(base_path)

    def safe_load_json(self, text: str):
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        match = re.search(r"\{[\s\S]*\}", text)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                return None

        return None

    def consolidate_llm_outputs(self, project_name: str):
        project_path = (
            self.base_path
            / "llm_outputs"
            / project_name
            / "insufficient_modularization"
            / self.engine
        )

        output_dir = (
            self.base_path
            / "consolidated_detection"
            / project_name
            / "insufficient_modularization"
            / self.engine
        )
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / "insufficient_modularization_llm.json"

        if not project_path.exists():
            raise FileNotFoundError(f"Path not found: {project_path}")

        consolidated = []
        required_fields = {"class", "detection", "justification"}

        for file in project_path.glob("*.txt"):
            raw_text = file.read_text(encoding="utf-8")
            content = self.safe_load_json(raw_text)

            if content is None:
                print(f"Warning: Could not parse JSON in {file}")
                continue

            if not required_fields.issubset(content):
                print(f"Warning: Missing required fields in {file}")
                continue

            cls_full_name = content.get("class")
            consolidated.append({
                "identifier": cls_full_name,
                "detection": content.get("detection"),
                "justification": content.get("justification"),
            })

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(consolidated, f, indent=4, ensure_ascii=False)

        return output_file

    def consolidate_designite_outputs(self, project_name: str):
        csv_file = self.base_path / "metrics" / project_name / "DesignSmells.csv"
        output_dir = (
            self.base_path
            / "consolidated_detection"
            / project_name
            / "insufficient_modularization"
            / self.engine
        )
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / "insufficient_modularization_designite.json"

        if not csv_file.exists():
            raise FileNotFoundError(f"File not found: {csv_file}")

        temp_dict = {}
        with open(csv_file, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("Smell") == "Insufficient Modularization":
                    pkg = row.get("Package")
                    cls_name = row.get("Class")
                    identifier = f"{pkg}.{cls_name}"
                    if identifier not in temp_dict:
                        temp_dict[identifier] = {
                            "identifier": identifier,
                            "detection": True,
                            "justification": row.get("Description")
                        }

        consolidated = list(temp_dict.values())

        with open(output_file, "w", encoding="utf-8") as out:
            json.dump(consolidated, out, indent=4, ensure_ascii=False)

        return output_file

    def load_consolidated_json(self, file_path: str):
        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)

        id_dict = {}
        for entry in data:
            detected = entry.get("detection", False)
            identifier = entry.get("identifier")
            id_dict[identifier] = detected

        return id_dict

    def get_all_identifiers(self, llm_dict: dict, designite_dict: dict):
        return set(llm_dict.keys()) | set(designite_dict.keys())

    def classify_identifier(self, llm_detected: bool, designite_detected: bool):
        if llm_detected and designite_detected:
            return "TP"
        elif not llm_detected and not designite_detected:
            return "TN"
        elif llm_detected and not designite_detected:
            return "FP"
        else:
            return "FN"

    def compute_confusion_matrix(self, llm_file: str, designite_file: str):
        llm_dict = self.load_consolidated_json(llm_file)
        designite_dict = self.load_consolidated_json(designite_file)

        all_ids = self.get_all_identifiers(llm_dict, designite_dict)
        counts = {"TP": 0, "TN": 0, "FP": 0, "FN": 0}

        for identifier in all_ids:
            llm_detected = llm_dict.get(identifier, False)
            designite_detected = designite_dict.get(identifier, False)
            category = self.classify_identifier(llm_detected, designite_detected)
            counts[category] += 1

        return counts

    def generate_metrics_file(self, llm_file: str, designite_file: str):
        confusion_matrix = self.compute_confusion_matrix(llm_file, designite_file)
        TP = confusion_matrix["TP"]
        TN = confusion_matrix["TN"]
        FP = confusion_matrix["FP"]
        FN = confusion_matrix["FN"]

        accuracy = (TP + TN) / (TP + TN + FP + FN) if (TP + TN + FP + FN) > 0 else 0.0
        precision = TP / (TP + FP) if (TP + FP) > 0 else 0.0
        recall = TP / (TP + FN) if (TP + FN) > 0 else 0.0
        f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

        metrics_data = {
            "confusion_matrix": confusion_matrix,
            "metrics": {
                "accuracy": round(accuracy, 3),
                "precision": round(precision, 3),
                "recall": round(recall, 3),
                "f1": round(f1, 3)
            }
        }

        output_dir = (
            self.base_path
            / "consolidated_detection"
            / self.project_name
            / "insufficient_modularization"
            / self.engine
        )
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / "insufficient_modularization_metrics.json"

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(metrics_data, f, indent=4, ensure_ascii=False)

        return output_file
