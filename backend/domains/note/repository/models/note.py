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