from application.helpers import pretty_cas_zpravy
from application import db
from io import BytesIO
from openpyxl import Workbook
from datetime import datetime
from application import socketio
from application.settings_handling import get_last_n


class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(2000))
    datetime = db.Column(db.DateTime, default=datetime.now)
    author = db.Column(db.String(100))
    category = db.Column(db.String(50)) # posadka, org, connection

    
    def as_dict(self) -> dict:
        as_dict = {
            "author": self.author,
            "content": self.content,
            "datetime": self.datetime.isoformat(),
            "pretty_time": pretty_cas_zpravy(self.datetime),
            "category": self.category
        }
        return as_dict

    
    def save_and_send(self):
        #saving
        db.session.add(self)
        db.session.commit()
    
        #sending
        self_as_dict = self.as_dict()
        socketio.send(self_as_dict)
        
        
    @staticmethod
    def get_history_on_join() -> list[dict]:

        last_n = get_last_n()
        messages = Message.get_all()[-last_n:]
        result = []
        for message in messages:
            m = message.as_dict()
            m["time"] = pretty_cas_zpravy(message.datetime)
            result.append(m)
        
        return result


    @staticmethod
    def get_all() -> list["Message"]:
        return db.session.scalars(db.select(Message)).all()
    
    
    @staticmethod
    def export_messages() -> BytesIO:
        messages = Message.get_all()

        wb = Workbook()
        ws = wb.active
        ws.title = "messages"

        # Write header
        ws.append(["id", "category", "datetime", "author", "content"])

        # Write data rows
        for message in messages:
            ws.append([message.id, message.category, message.datetime, message.author, message.content])

        # Save workbook to a BytesIO stream and return it
        xlsx_stream = BytesIO()
        wb.save(xlsx_stream)
        xlsx_stream.seek(0)

        return xlsx_stream
    
    
    @staticmethod
    def delete_all():
        for message in Message.get_all():
            db.session.delete(message)
        db.session.commit()
