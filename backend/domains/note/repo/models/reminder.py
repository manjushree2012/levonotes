from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
import humanize

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