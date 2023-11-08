import random
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from .database import engine

Base = declarative_base()


class Event(Base):
    __tablename__ = 'events'

    event_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    start = Column(DateTime, default=func.now())
    end = Column(DateTime, default=func.now())
    note = Column(String)
    repeat = Column(String, nullable=True)
    is_full_day = Column(Boolean, server_default='false', nullable=False)
    repeat_interval = Column(Integer, server_default='1', nullable=False)
    note = Column(String)
    color = Column(String, nullable=True)
    is_repeated_child = Column(Boolean, default=False)


# Create the 'events' table in your database
Base.metadata.create_all(bind=engine)
