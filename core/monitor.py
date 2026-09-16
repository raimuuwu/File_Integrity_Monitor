import time
from pathlib import Path
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from core.hasher import calculate_sha256


class FIMHandler(FileSystemEventHandler):
    def __init__(self, db_file_path: str = "baseline.json"):
        super().__init__()
        self.db_path = str(Path(db_file_path).resolve())

    def on_created(self, event):
        if event.is_directory or str(Path(event.src_path).resolve()) == self.db_path:
            return

        file_hash = calculate_sha256(event.src_path)
        print(f"[+] [CREATED] File: {event.src_path} | SHA-256: {file_hash}")

    def on_modified(self, event):
        if event.is_directory or str(Path(event.src_path).resolve()) == self.db_path:
            return

        file_hash = calculate_sha256(event.src_path)
        print(f"[*] [MODIFIED] File: {event.src_path} | SHA-256: {file_hash}")

    def on_deleted(self, event):
        if event.is_directory or str(Path(event.src_path).resolve()) == self.db_path:
            return

        print(f"[-] [DELETED] File: {event.src_path}")


def start_live_monitoring(target_directory: str, db_file_path: str = "baseline.json"):
    event_handler = FIMHandler(db_file_path=db_file_path)
    observer = Observer()

    observer.schedule(event_handler, path=target_directory, recursive=True)

    print(f"[*] Starting live monitoring on: {target_directory}")
    print("[*] Press Ctrl+C to stop...\n")

    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[*] Stopping live monitoring...")
        observer.stop()

    observer.join()