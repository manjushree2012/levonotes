from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

url = URL.create(
    drivername = "postgresql",
    username   = "postgres.qcfnkpxhcboxpwncrebf",
    host       = "aws-0-ap-south-1.pooler.supabase.com",
    database   = "postgres",
    password   = "1Magic-code1111",
    port       = "6543"
)
engine = create_engine(url)
connection = engine.connect()

Base = declarative_base()
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

session.commit()


class Repository:
    def create():
        newNote = Note(
            title="Mohammed",
            content="ahmed_email@gmail.com"
        )
        session.add(newNote)
        session.commit()




from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Text

Base = declarative_base()

class Note(Base):
    __tablename__ = 'notes'

    id = Column(Integer(), primary_key=True)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)

    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)