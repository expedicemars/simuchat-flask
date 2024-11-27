from pathlib import Path

def messages_history_folder_path() -> Path:
    return Path.cwd() / "messages_history"

def current_messages_path() -> Path:
    return messages_history_folder_path() / "current_messages.json"

def history_path():
    return messages_history_folder_path() / "history.json"

def settings_path():
    return Path.cwd() / "settings/settings.json"
