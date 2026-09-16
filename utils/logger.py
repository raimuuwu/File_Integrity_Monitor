from datetime import datetime
from pathlib import Path

def log_event(event_type: str, file_path: str, file_hash: str = None, log_dir: str = "logs",) -> None:

    log_folder = Path(log_dir)
    log_folder.mkdir(parents=True, exist_ok=True)

    log_file = log_folder / "fim_events.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_entry = f"[{timestamp}] [{event_type.upper()}] File: {file_path}"
    if file_hash:
        log_entry += f" | SHA-256: {file_hash}"

    try:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(log_entry + "\n")
    except OSError as e:
        print(f"[!] Failed to write log to file: {e}")