from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, Text

from datetime import datetime

from dotenv import load_dotenv
import os

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

class Note(Base):
    __tablename__ = 'notes'

    id = Column(Integer(), primary_key=True)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)

    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

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
    return new_note


