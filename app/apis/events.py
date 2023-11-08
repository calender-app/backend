
from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import SessionLocal
from repositories.eventRepository import create_event, get_event, get_events, update_event, delete_event
from schemas.events import EventCollectionResponse, EventCreate, EventObjectResponse
from fastapi.security import HTTPBearer

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# TODO use appConstant for error or success message


auth_scheme = HTTPBearer()


@router.post("/events/", response_model=EventObjectResponse)
def create_event_api(event: EventCreate, db: Session = Depends(get_db)):
    event = create_event(db, event)
    return {"success": True, "message": "Event successfully created"}


@router.get("/events/", response_model=EventCollectionResponse)
def read_events(skip: int = 0, limit: int = 100, filter_string=None, db: Session = Depends(get_db), currentDate: str = None):
    events = get_events(db, skip, limit, filter_string, currentDate)
    events_list = [event.__dict__ for event in events]
    return {"success": True, "message": "Events successfully fetched", "data": events_list}


@router.put("/events/{event_id}", response_model=EventObjectResponse)
def update_event_api(event_id: int, event: EventCreate, db: Session = Depends(get_db)):

    current_event = get_event(db, event_id)
    print(current_event)
    if current_event and current_event.is_repeated_child and current_event.repeat != event.repeat:
        raise HTTPException(
            status_code=400, detail="Could not update repeat of child event")

    event = update_event(db, event_id, event)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"success": True, "message": "Event successfully updated"}


@router.delete("/events/{event_id}",)
def delete_event_api(event_id: int, db: Session = Depends(get_db)):
    delete_event(db, event_id)
    return {"success": True, "message": "Event successfully deleted", "data": {}}
