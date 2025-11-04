from datetime import datetime
import json
from application.helpers import pretty_cas_zpravy


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
        
        ## todo sql
        # result = [m.as_dict() for m in all]
        # with open(current_messages_path(), "w") as file:
        #     file.write(json.dumps(result, indent=4))
    
        # #sending
        # self_as_dict = self.as_dict()
        # self_as_dict["time"] = pretty_cas_zpravy()
        # flask_socketio.send(self_as_dict, broadcast=True)
        
        
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
        pass
        ## TODO sw
        # with open(current_messages_path()) as file:
        #     messages = json.load(file)
        # resut = []
        # for msg in messages:
        #     m = Message(name = msg["name"], text=msg["text"], type=msg["type"], time=datetime.fromisoformat(msg["time"]))
        #     resut.append(m)
        # return resut