from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from datetime import datetime
import humanize

Base = declarative_base()

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


