from pathlib import Path

def settings_path():
    return Path.cwd() / "settings/settings.json"

def settings_example_path():
    return Path.cwd() / "settings/settings.json.example"