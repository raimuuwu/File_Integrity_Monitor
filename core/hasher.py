import hashlib
from typing import Optional

import config
#BUFFER_SIZE = 65536

def calculate_sha256(file_path: str) -> Optional[str]:
    try:
        hasher = hashlib.sha256()
        with open(file_path,"rb") as file:
            while True:
                chunk = file.read(config.BUFFER_SIZE)
                if not chunk:
                    break
                hasher.update(chunk)
        final_hash = hasher.hexdigest()
        return final_hash
    except (FileNotFoundError, PermissionError, OSError) as e:
        print(f"Error during operning '{file_path}': {e}")
        return None