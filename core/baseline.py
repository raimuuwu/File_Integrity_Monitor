import json
from pathlib import Path

from core.hasher import calculate_sha256


def create_baseline(target_directory: str, db_file_path: str = "baseline.json") -> bool:
    target_path = Path(target_directory)
    db_path = Path(db_file_path).resolve()

    if not target_path.exists() or not target_path.is_dir():
        print(f"[!] Target directory does not exist or is not a directory: {target_directory}")
        return False

    baseline_data = {}

    for path in target_path.rglob("*"):
        if path.is_file():
            if path.resolve() == db_path:
                continue

            print(f"[*] Processing file: {path}")

            file_hash = calculate_sha256(str(path))
            if file_hash is not None:
                baseline_data[str(path.resolve())] = file_hash

    try:
        with open(db_path, "w", encoding="utf-8") as f:
            json.dump(baseline_data, f, indent=4)
        print(f"[+] Baseline successfully saved ({len(baseline_data)} files hashed): {db_path}")
        return True
    except (FileNotFoundError, PermissionError, OSError) as e:
        print(f"[!] Error writing baseline file '{db_path}': {e}")
        return False