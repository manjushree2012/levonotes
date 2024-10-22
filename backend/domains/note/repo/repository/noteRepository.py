from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from dotenv import load_dotenv
import os

from domains.note.repo.models.note import Note, Reminder

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
        notes = session.query(Note).order_by(Note.updated_on.desc()).all()
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

def get_note(note_id):
    try:
        note = session.query(Note).filter(Note.id == note_id).first()
        if note:
            return note.to_dict()  # Return the note as a dictionary
        else:
            return None  # No note found for the given note_id
    except Exception as e:
        session.rollback()  # Rollback the session in case of an error
        raise e  # Raise the exception for handling by the caller

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

def create_reminder(data):
    # Create a new reminder
    new_reminder = Reminder(
        email=data['email'],
        message=data['message'],
        reminder_time=data['reminder_time'],
        note_id=data.get('note_id')  # This will be None if not provided
    )
    session.add(new_reminder)
    session.commit()

    return new_reminder.to_dict()

def update_reminder(reminder_id, data):
    # Update an existing reminder
    reminder = session.query(Reminder).filter(Reminder.id == reminder_id).first()
    if reminder:
        reminder.email = data['email']
        reminder.message = data['message']
        reminder.reminder_time = data['reminder_time']
        reminder.note_id = data.get('note_id', reminder.note_id)  # Update note_id if provided, else keep existing
        session.commit()

        return reminder.to_dict()
    else:
        return None

def get_reminder_from_note(note_id):
    try:
        reminder = session.query(Reminder).filter(Reminder.note_id == note_id).first()
        if reminder:
            return reminder.to_dict()  # Return the reminder as a dictionary
        else:
            return None  # No reminder found for the given note_id
    except Exception as e:
        session.rollback()  # Rollback the session in case of an error
        raise e  # Raise the exception for handling by the caller
