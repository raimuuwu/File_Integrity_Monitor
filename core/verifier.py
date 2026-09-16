import json
from pathlib import Path
from core.hasher import calculate_sha256


def verify_integrity(target_directory: str, db_file_path: str = "baseline.json") -> dict:
    results = {"modified": [], "created": [], "deleted": []}
    target_path = Path(target_directory)
    db_path = Path(db_file_path).resolve()

    try:
        with open(db_path, "r", encoding="utf-8") as f:
            db_file = json.load(f)
    except FileNotFoundError:
        print(f"[!] Baseline file '{db_path}' not found. Please run baseline creation first.")
        return results
    except json.JSONDecodeError:
        print(f"[!] Baseline file '{db_path}' is corrupted.")
        return results


    current_state = {}
    if target_path.exists() and target_path.is_dir():
        for path in target_path.rglob("*"):
            if path.is_file():
                if path.resolve() == db_path:
                    continue

                file_hash = calculate_sha256(str(path))
                if file_hash is not None:
                    current_state[str(path.resolve())] = file_hash


    for file_path, current_hash in current_state.items():
        if file_path in db_file:
            if current_hash != db_file[file_path]:
                results["modified"].append(file_path)
        else:
            results["created"].append(file_path)


    for file_path in db_file:
        if file_path not in current_state:
            results["deleted"].append(file_path)

    return results