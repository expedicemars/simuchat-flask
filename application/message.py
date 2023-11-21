from datetime import datetime
from .paths import messages_path
import json
from .settings_handling import get_datetime_zacatku
import flask_socketio

def pretty_cas_zpravy(time: datetime = None) -> str:
    datetime_zacatku = get_datetime_zacatku()
    datetime_zpravy = time if time else datetime.now()
    dt = datetime_zpravy - datetime_zacatku
    diff = dt.total_seconds()
    print(diff)
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
    
    def save(self):
        self_as_dict = self.as_dict()
        
        with open(messages_path()) as file:
            messages = json.load(file)
        messages.append(self_as_dict)
        with open(messages_path(), "w") as file:
            file.write(json.dumps(messages, indent=4))
    
    def send(self):
        self_as_dict = self.as_dict()
        self_as_dict["time"] = pretty_cas_zpravy()
        flask_socketio.send(self_as_dict, broadcast=True)
    
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
        with open(messages_path()) as file:
            messages = json.load(file)
        resut = []
        for msg in messages:
            m = Message(name = msg["name"], text=msg["text"], type=msg["type"], time=datetime.fromisoformat(msg["time"]))
            resut.append(m)
        return resut