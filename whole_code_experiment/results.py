import csv
import json
from pathlib import Path


BASE_DIR = Path("data/processed")
CANDIDATES_DIR = BASE_DIR / "candidates_sampled"
LLM_OUTPUTS_DIR = BASE_DIR / "llm_outputs"
OUTPUT_DIR = BASE_DIR / "results"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SMELLS = {
    "god_component": "god_component_sample.csv",
    "unstable_dependency": "unstable_dependency_sample.csv",
    "insufficient_modularization": "insufficient_modularization_sample.csv",
    "hublike_modularization": "hublike_modularization_sample.csv",
}

def load_detection(llm_file: Path) -> bool:
    content = llm_file.read_text(encoding="utf-8").strip()

    if not content:
        return False

    try:
        data = json.loads(content)
        return bool(data.get("detection", False))
    except json.JSONDecodeError:
        pass

    start = content.find("{")
    end = content.rfind("}")

    if start == -1 or end == -1 or end <= start:
        return False

    try:
        data = json.loads(content[start:end + 1])
        return bool(data.get("detection", False))
    except json.JSONDecodeError:
        return False

def compute_metrics(tp, tn, fp, fn):
    total = tp + tn + fp + fn

    accuracy = (tp + tn) / total if total else 0.0
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = (
        2 * precision * recall / (precision + recall)
        if (precision + recall)
        else 0.0
    )

    return {
        "accuracy": round(accuracy, 3),
        "precision": round(precision, 3),
        "recall": round(recall, 3),
        "f1": round(f1, 3),
    }


def process_smell(smell_name: str, csv_name: str):
    csv_path = CANDIDATES_DIR / csv_name
    llm_dir = LLM_OUTPUTS_DIR / smell_name / "deepseek"

    tp = tn = fp = fn = 0

    with csv_path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            label = int(row["label"])
            prompt_file = Path(row["prompt_file"])
            llm_file = llm_dir / prompt_file.name

            detection = load_detection(llm_file)
            print(f"Processed: {llm_file}")

            prediction = 1 if detection else 0

            if label == 1 and prediction == 1:
                tp += 1
            elif label == 0 and prediction == 0:
                tn += 1
            elif label == 0 and prediction == 1:
                fp += 1
            elif label == 1 and prediction == 0:
                fn += 1

    metrics = compute_metrics(tp, tn, fp, fn)

    result = {
        "confusion_matrix": {
            "TP": tp,
            "TN": tn,
            "FP": fp,
            "FN": fn,
        },
        "metrics": metrics,
    }

    return result


def main():
    all_results = {}

    for smell, csv_file in SMELLS.items():
        print(f"Processing smell: {smell}")
        result = process_smell(smell, csv_file)

        all_results[smell] = result

        # Save per-smell result
        output_file = OUTPUT_DIR / f"{smell}_results.json"
        with output_file.open("w", encoding="utf-8") as f:
            json.dump(result, f, indent=4)

    # Optional: save aggregated results
    aggregated_file = OUTPUT_DIR / "all_smells_results.json"
    with aggregated_file.open("w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=4)

    print("\nDone. Results saved in:", OUTPUT_DIR.resolve())


if __name__ == "__main__":
    main()
