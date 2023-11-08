from datetime import timedelta, datetime
from sqlalchemy.orm import Session

from app.constants import appConstants
from ..database.models import Event
from ..schemas.events import EventCreate
from dateutil.parser import parse

from sqlalchemy_filters import apply_filters
from dateutil.relativedelta import relativedelta
from ..utilities.index import get_random_color


def event_to_dict(event: Event) -> dict:
    return {
        "title": event.title,
        "description": event.description,
        "start": event.start,
        "end": event.end,
        "note": event.note,
        "repeat": event.repeat,
        "is_full_day": event.is_full_day,
        "repeat_interval": event.repeat_interval,
    }


def generate_recurring_events(db: Session, event: Event, event_create: EventCreate):
    recurring_events = []
    color = get_random_color()
    for i in range(1, appConstants.RECURRING_LIMITS[event_create.repeat]):
        new_start = event_create.start
        new_end = event_create.end

        if event_create.repeat == "DAILY":
            new_start += timedelta(days=i * event_create.repeat_interval)
            new_end += timedelta(days=i * event_create.repeat_interval)
        elif event_create.repeat == "WEEKLY":
            new_start += timedelta(weeks=i * event_create.repeat_interval)
            new_end += timedelta(weeks=i * event_create.repeat_interval)
        elif event_create.repeat == "MONTHLY":
            new_start += relativedelta(months=i * event_create.repeat_interval)
            new_end += relativedelta(months=i * event_create.repeat_interval)

        recurring_event = Event(**event_create.dict())
        recurring_event.start = new_start
        recurring_event.end = new_end
        recurring_event.is_repeated_child = True
        recurring_event.color = color
        recurring_events.append(recurring_event)

    db.add_all(recurring_events)
    db.commit()


def create_event(db: Session, event_create: EventCreate):
    db_event = Event(**event_create.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)

    if event_create.repeat != "NEVER":
        generate_recurring_events(db, db_event, event_create)

    return db_event


def get_event(db: Session, event_id: int):
    return db.query(Event).filter(Event.event_id == event_id).first()


def get_events(db: Session, skip: int = 0, limit: int = 10, filter_string=None, current_date=None):

    current_date = parse(current_date)
    year = current_date.year
    month = current_date.month

    # Calculate the first day of the current month
    start_of_month = datetime(year, month, 1)
    start_of_next_month = start_of_month + relativedelta(months=1)
    # print(start_of_month)
    # TODO: move to utility
    query = db.query(Event)
    query = query.filter(Event.start >= start_of_month,
                         Event.start < start_of_next_month)

    if filter_string:
        filter_spec = [{
            'or': [
                {'model': "Event",
                 "field": "title",
                 "op": "ilike",
                 "value": f"%{filter_string}%"
                 },
                {'model': "Event",
                 "field": "description",
                 "op": "ilike",
                 "value": f"%{filter_string}%"
                 },
                {'model': "Event",
                 "field": "note",
                 "op": "ilike",
                 "value": f"%{filter_string}%"
                 },
            ]

        }]
        query = apply_filters(query, filter_spec)
    events = query.offset(skip).limit(limit).all()
    return events


def update_event(db: Session, event_id: int, event: EventCreate):
    db_event = db.query(Event).filter(Event.event_id == event_id).first()
    for key, value in event.dict().items():
        setattr(db_event, key, value)
    db.commit()
    db.refresh(db_event)
    return db_event


def delete_event(db: Session, event_id: int):
    db_event = db.query(Event).filter(Event.event_id == event_id).first()
    if (db_event is None):
        return False
    if db_event:
        db.delete(db_event)
        db.commit()
    return True
