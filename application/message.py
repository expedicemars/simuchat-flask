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
    status = db.Column(db.String(20), nullable=False, default="none")

    
    def as_dict(self) -> dict:
        as_dict = {
            "id": self.id,
            "author": self.author,
            "content": self.content,
            "datetime": self.datetime.isoformat(),
            "pretty_time": pretty_cas_zpravy(self.datetime),
            "category": self.category,
            "status": self.status
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
        messages = Message.get_before(None, last_n)
        return Message.messages_as_dict(messages)


    @staticmethod
    def get_before(before_id: int | None, limit: int) -> list["Message"]:
        query = db.select(Message).order_by(Message.id.desc()).limit(limit)
        if before_id is not None:
            query = (
                db.select(Message)
                .where(Message.id < before_id)
                .order_by(Message.id.desc())
                .limit(limit)
            )
        return list(reversed(db.session.scalars(query).all()))


    @staticmethod
    def has_before(before_id: int) -> bool:
        return db.session.scalar(
            db.select(Message.id)
            .where(Message.id < before_id)
            .limit(1)
        ) is not None


    @staticmethod
    def messages_as_dict(messages: list["Message"]) -> list[dict]:
        result = []
        for message in messages:
            m = message.as_dict()
            m["time"] = pretty_cas_zpravy(message.datetime)
            result.append(m)
        return result


    @staticmethod
    def get_all() -> list["Message"]:
        return db.session.scalars(
            db.select(Message).order_by(Message.id)
        ).all()
    
    
    @staticmethod
    def export_messages() -> BytesIO:
        messages = Message.get_all()

        wb = Workbook()
        ws = wb.active
        ws.title = "messages"

        # Write header
        ws.append(["id", "category", "datetime", "author", "content", "status"])

        # Write data rows
        for message in messages:
            ws.append([
                message.id,
                message.category,
                message.datetime,
                message.author,
                message.content,
                message.status
            ])

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
