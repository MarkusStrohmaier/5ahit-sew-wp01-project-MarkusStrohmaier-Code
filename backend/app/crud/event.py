from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.event import Event
from app.models.location import Location
from app.schemas.event import EventCreate, EventUpdate
from app.models.user import User


def create_event(db: Session, event: EventCreate, user: User):
    location = (
        db.query(Location)
        .filter(Location.id == event.location_id, Location.user_id == user.id)
        .first()
    )
    if not location:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Location not found or not owned by user")

    db_event = Event(
        title=event.title,
        date=event.date,
        time=event.time,
        description=event.description,
        ticket_capacity=event.ticket_capacity,
        location_id=event.location_id
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def get_event(db: Session, event_id: int, user: User):
    event = (
        db.query(Event)
        .join(Location)
        .filter(Event.id == event_id, Location.user_id == user.id)
        .first()
    )
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    return event


def get_events(db: Session, user: User):
    return (
        db.query(Event)
        .join(Location)
        .filter(Location.user_id == user.id)
        .all()
    )


def update_event(db: Session, event_id: int, event: EventUpdate, user: User):
    db_event = (
        db.query(Event)
        .join(Location)
        .filter(Event.id == event_id, Location.user_id == user.id)
        .first()
    )
    if not db_event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    if event.location_id is not None:
        new_location = (
            db.query(Location)
            .filter(Location.id == event.location_id, Location.user_id == user.id)
            .first()
        )
        if not new_location:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="New location not found or not owned by user")

    for key, value in event.dict(exclude_unset=True).items():
        setattr(db_event, key, value)

    db.commit()
    db.refresh(db_event)
    return db_event


def delete_event(db: Session, event_id: int, user: User):
    db_event = (
        db.query(Event)
        .join(Location)
        .filter(Event.id == event_id, Location.user_id == user.id)
        .first()
    )
    if not db_event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    db.delete(db_event)
    db.commit()
    return db_event
