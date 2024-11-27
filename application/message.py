from datetime import datetime, timedelta
from .paths import current_messages_path, history_path
import json
from .settings_handling import get_datetime_zacatku, get_pocet_zprav_manual, get_pocet_zprav_auto
import flask_socketio
from flask import current_app

def pretty_cas_zpravy(time: datetime = None) -> str:
    datetime_zacatku = get_datetime_zacatku()
    datetime_zpravy = time if time else datetime.now()
    dt = datetime_zpravy - datetime_zacatku
    diff = dt.total_seconds()
    sign = ""
    if diff < 0:
        sign = "- "
    diff = abs(diff)
    hours = int(diff / 3600)
    leftover = diff - hours*3600
    minutes = int(leftover/60)
    leftover = leftover - minutes*60
    sec = int(leftover)
    return f"{sign}{str(hours).rjust(2, '0')} : {str(minutes).rjust(2, '0')} : {str(sec).rjust(2, '0')}"

def archivovat_vse() -> None:
    with open(current_messages_path()) as current:
        current: list[dict] = json.load(current)
    with open(history_path()) as history:
        history: list[dict] = json.load(history)
    
    new_history = history + current
    with open(current_messages_path(), "w") as c:
        c.write(json.dumps([], indent=4))
    with open(history_path(), "w") as h:
        h.write(json.dumps(new_history, indent=4))


def archivovat() -> None:
    with open(current_messages_path()) as current:
        current: list[dict] = json.load(current)
    with open(history_path()) as history:
        history: list[dict] = json.load(history)
    
    n = get_pocet_zprav_manual()
    new_current = current[-n:]
    new_history = current[:-n]
    whole_history = history + new_history
    
    with open(current_messages_path(), "w") as c:
        c.write(json.dumps(new_current, indent=4))
    with open(history_path(), "w") as h:
        h.write(json.dumps(whole_history, indent=4))
    
    with current_app.app_context():
        current_app.extensions["socketio"].emit("archivovani", {"pocet": get_pocet_zprav_manual()})
        

class Message():
    def __init__(self, name: str, text: str, type: str, time: datetime = None) -> None:
        self.name = name
        self.text = text
        self.type = type
        self.time = time if time else datetime.now()
    
    def as_dict(self) -> dict:
        as_dict = {
            "name": self.name,
            "text": self.text,
            "time": self.time.isoformat(),
            "type": self.type
        }
        return as_dict

    
    def save_and_send(self):
        #saving
        all = Message.get_all()
        all.append(self)
        
            
        result = [m.as_dict() for m in all]
        with open(current_messages_path(), "w") as file:
            file.write(json.dumps(result, indent=4))
    
        #sending
        self_as_dict = self.as_dict()
        self_as_dict["time"] = pretty_cas_zpravy()
        flask_socketio.send(self_as_dict, broadcast=True)
        
        if len(all) > get_pocet_zprav_auto():
            archivovat()
        
        
    @staticmethod
    def get_history_on_join() -> str:
        messages = Message.get_all()
        result = []
        for message in messages:
            m = message.as_dict()
            m["time"] = pretty_cas_zpravy(message.time)
            result.append(m)
        
        return json.dumps(result)

    @staticmethod
    def get_all() -> list["Message"]:
        with open(current_messages_path()) as file:
            messages = json.load(file)
        resut = []
        for msg in messages:
            m = Message(name = msg["name"], text=msg["text"], type=msg["type"], time=datetime.fromisoformat(msg["time"]))
            resut.append(m)
        return resut