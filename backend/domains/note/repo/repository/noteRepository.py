from domains.note.repo.models.note import Note, Reminder
from domains.note.repo.repository.setup import session
from datetime import datetime

def get_due_reminders():
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
    

