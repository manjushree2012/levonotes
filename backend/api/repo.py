from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, Text


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


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()