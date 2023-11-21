from pathlib import Path

def messages_path():
    return Path.cwd() / "messages.json"

def settings_path():
    return Path.cwd() / "settings.json"