from domains.note.repo.models.note import Reminder
from domains.note.repo.repository.setup import session

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
