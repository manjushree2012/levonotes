from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, Text

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from datetime import datetime

from dotenv import load_dotenv
import os

import humanize

load_dotenv()

url = URL.create(
    drivername = "postgresql",
    username   = os.getenv('DB_USER'),
    host       = os.getenv('DB_HOST'),
    database   = os.getenv('DB_NAME'),
    password   = os.getenv('DB_PASSWORD'),
    port       = os.getenv('DB_PORT')
)

engine = create_engine(url)
connection = engine.connect()

Base = declarative_base()

class Reminder(Base):
    __tablename__ = 'reminders'

    id = Column(Integer(), primary_key=True)
    email = Column(String(100), nullable=False)
    message = Column(Text, nullable=False)
    reminder_time = Column(DateTime(), nullable=False)
    note_id = Column(Integer, ForeignKey('notes.id'))

    note = relationship("Note", back_populates="reminder")

    def to_dict(self):
        return {
            'id': self.id,
            'email' : self.email,
            'message' : self.message,
            'reminder_time' : self.reminder_time,
            'reminder_time_readable' : humanize.naturaltime(self.reminder_time) if self.reminder_time else None,
        }

class Note(Base):
    __tablename__ = 'notes'

    id = Column(Integer(), primary_key=True)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    reminder = relationship("Reminder", uselist=False, back_populates="note")

    def to_dict(self):
        return {
            'id'                 : self.id,
            'title'              : self.title,
            'content'            : self.content,
            'created_at'         : self.created_on,
            'updated_on'         : self.updated_on,
            'updated_at_readable': humanize.naturaltime(self.updated_on) if self.updated_on else None,

            'reminder'           : self.reminder.to_dict() if self.reminder else None,            
        }


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def get_due_reminders():
    from datetime import datetime
    now = datetime.now()

    due_reminders = session.query(Reminder).filter(Reminder.reminder_time <= now).all()

    return due_reminders

def create_note(data):
    new_note = Note(
        title=data['title'],
        content=data['content']
    )
    session.add(new_note)
    session.commit()

    note_dict = {
        'id': new_note.id,
        'title': new_note.title,
        'content': new_note.content,
        'created_on': new_note.created_on,
        'updated_on': new_note.updated_on
    }
    return note_dict

def delete_note(note_id):
    try:
        note = session.query(Note).filter(Note.id == note_id).first()
        if note:
            session.delete(note)
            session.commit()
            return True
        else:
            return False
    except Exception as e:
        session.rollback()
        raise e

def get_all_notes():
    try:
        notes = session.query(Note).all()
        return [note.to_dict() for note in notes]
    except Exception as e:
        session.rollback()
        raise e


def update_note(note_id, data):
    try:
        note = session.query(Note).filter(Note.id == note_id).first()
        if note:
            note.title = data['title']
            note.content = data['content']
            note.updated_on = datetime.utcnow()
            session.commit()

            return {
                'id': note.id,
                'title': note.title,
                'content': note.content,
                'created_on': note.created_on,
                'updated_on': note.updated_on
            }
        else:
            return None
    except Exception as e:
        session.rollback()
        raise e

def search_notes(query):
    # Use SQLAlchemy to filter notes based on the search query
    results = session.query(Note).filter(Note.content.ilike(f'%{query}%')).all()
    return [note.to_dict() for note in results]
    
def add_reminder(data):
    new_reminder = Reminder(
        email=data['email'],
        message=data['message'],
        reminder_time=data['reminder_time'],
        note_id=data.get('note_id')  # This will be None if not provided
    )
    session.add(new_reminder)
    session.commit()

    return new_reminder.to_dict()
