from pathlib import Path

def current_messages_path():
    return Path.cwd() / "messages_history" / "current_messages.json"

def history_path():
    return Path.cwd() / "messages_history" / "history.json"

def settings_path():
    return Path.cwd() / "settings.json"