import pytest
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.location import Location
from app.models.event import Event
from app.schemas.event import EventCreate, EventUpdate
from app.crud.event import create_event, get_event, get_events, update_event, delete_event


@pytest.fixture
def test_location(db: Session):
    location = Location(
        name="Test Location",
        address="123 Test St",
        capacity=100
    )
    db.add(location)
    db.commit()
    db.refresh(location)
    return location


@pytest.fixture
def test_event(db: Session, test_location: Location):
    event = Event(
        title="Initial Event",
        date=datetime.utcnow(),
        time="12:00",
        description="Initial test event",
        ticket_capacity=50,
        location_id=test_location.id
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def test_create_event(db: Session, test_location: Location):
    event_in = EventCreate(
        title="New Event",
        date=datetime.utcnow(),
        time="18:00",
        description="A new test event",
        ticket_capacity=75,
        location_id=test_location.id
    )
    event = create_event(db, event_in)
    assert isinstance(event.id, int)
    assert event.title == "New Event"
    assert event.location_id == test_location.id


def test_create_event_invalid_location(db: Session):
    event_in = EventCreate(
        title="Invalid Location Event",
        date=datetime.utcnow(),
        time="18:00",
        description="Should fail",
        ticket_capacity=50,
        location_id=99999
    )
    with pytest.raises(HTTPException) as exc:
        create_event(db, event_in)
    assert exc.value.status_code == 404


def test_get_event(db: Session, test_event: Event):
    fetched = get_event(db, test_event.id)
    assert fetched.id == test_event.id
    assert fetched.title == test_event.title


def test_get_events(db: Session, test_event: Event):
    events = get_events(db)
    ids = [e.id for e in events]
    assert test_event.id in ids


def test_update_event(db: Session, test_event: Event, test_location: Location):
    update_data = EventUpdate(
        title="Updated Event",
        time="20:00",
        ticket_capacity=150
    )
    updated = update_event(db, test_event.id, update_data)
    assert updated.title == "Updated Event"
    assert updated.time == "20:00"
    assert updated.ticket_capacity == 150


def test_update_event_invalid_location(db: Session, test_event: Event):
    update_data = EventUpdate(location_id=99999)
    with pytest.raises(HTTPException) as exc:
        update_event(db, test_event.id, update_data)
    assert exc.value.status_code == 404


def test_delete_event(db: Session, test_event: Event):
    deleted = delete_event(db, test_event.id)
    assert deleted.id == test_event.id
    with pytest.raises(HTTPException):
        get_event(db, test_event.id)
