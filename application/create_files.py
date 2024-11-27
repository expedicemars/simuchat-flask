from .paths import current_messages_path, history_path, messages_history_folder_path
import json

def ensure_messages_files() -> None:
    p = messages_history_folder_path()
    if not p.exists():
        p.mkdir()
    
    p = current_messages_path()
    if not p.exists():
        p.touch()
        with open(p, "w") as file:
            file.write(json.dumps([], indent=4))

    p = history_path()
    if not p.exists():
        p.touch()
        with open(p, "w") as file:
            file.write(json.dumps([], indent=4))