from .paths import current_messages_path, history_path, messages_history_folder_path
import json

def create_messages_file() -> None:
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