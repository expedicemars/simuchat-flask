from .paths import messages_path
import json

def create_messages_file() -> None:
    p = messages_path()
    if not p.exists():
        p.touch()
        with open(p, "w") as file:
            file.write(json.dumps([], indent=4))