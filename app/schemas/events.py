from pydantic import BaseModel, validator
from datetime import datetime, timedelta
from typing import Optional


class EventBase(BaseModel):
    event_id: Optional[int]
    title: str
    description: str
    start: datetime = datetime.now()+timedelta(minutes=1)
    end: datetime = datetime.now()+timedelta(minutes=61)
    note: str
    repeat: str
    is_full_day: bool = False
    repeat_interval: int = 1


class EventCreate(EventBase):

    @validator("start", "end", pre=True)
    def date_validation(cls, value):
        now = datetime.now()
        if datetime.fromisoformat(value) < now:
            raise ValueError("Event can not be in past time")
        return value


class Event(BaseModel):
    event_id: Optional[int]
    title: str
    description: str
    start: datetime = datetime.now()
    end: datetime = datetime.now()+timedelta(hours=1)
    note: str
    repeat: str
    is_full_day: bool = False
    repeat_interval: int = 1
    is_repeated_child: bool = False
    color: Optional[str]


class EventCollectionResponse(BaseModel):
    success: bool
    message: str
    data: list[Event]


class EventObjectResponse(BaseModel):
    success: bool
    message: str
