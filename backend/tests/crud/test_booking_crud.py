import pytest
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.crud.booking import create_booking, get_booking, get_bookings, update_booking, delete_booking
from app.models.booking import Booking
from app.models.user import User
from app.models.event import Event
from app.schemas.booking import BookingCreate, BookingUpdate

import uuid

@pytest.fixture
def test_user(db: Session):
    unique_username = f"testuser_{uuid.uuid4().hex[:8]}" #dynamischer Benutzernamen um UNIQUE-Constraint Constraint zu umgehen
    user = User(username=unique_username, email=f"{unique_username}@example.com", hashed_password="hashedpw")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def test_event(db: Session):
    event = Event(title="Test Event", date=datetime.now(), ticket_capacity=100)
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

@pytest.fixture
def test_booking(db: Session, test_user: User, test_event: Event):
    booking_in = BookingCreate(user_id=test_user.id, event_id=test_event.id, booking_date=datetime.now())
    booking = create_booking(db, booking_in)
    return booking

def test_create_booking(db: Session, test_user: User, test_event: Event):
    booking_in = BookingCreate(user_id=test_user.id, event_id=test_event.id, booking_date=datetime.now())
    booking = create_booking(db, booking_in)

    assert isinstance(booking.booking_number, int)
    assert booking.user_id == test_user.id
    assert booking.event_id == test_event.id

def test_get_booking(db: Session, test_booking: Booking):
    fetched = get_booking(db, test_booking.booking_number)
    assert fetched.booking_number == test_booking.booking_number
    assert fetched.user_id == test_booking.user_id

def test_get_bookings(db: Session, test_booking: Booking):
    all_bookings = get_bookings(db)
    booking_numbers = [b.booking_number for b in all_bookings]
    assert test_booking.booking_number in booking_numbers

def test_update_booking(db: Session, test_booking: Booking, test_event: Event, test_user: User):
    update_data = BookingUpdate(user_id=test_user.id, event_id=test_event.id)
    updated = update_booking(db, test_booking.booking_number, update_data)
    assert updated.user_id == test_user.id
    assert updated.event_id == test_event.id

def test_delete_booking(db: Session, test_booking: Booking):
    deleted = delete_booking(db, test_booking.booking_number)
    assert deleted.booking_number == test_booking.booking_number

    with pytest.raises(HTTPException):
        get_booking(db, test_booking.booking_number)

def test_create_booking_invalid_user(db: Session, test_event: Event):
    from fastapi import HTTPException
    from pytest import raises
    booking_in = BookingCreate(user_id=9999, event_id=test_event.id, booking_date=datetime.now())
    with raises(HTTPException):
        create_booking(db, booking_in)

def test_create_booking_invalid_event(db: Session, test_user: User):
    from fastapi import HTTPException
    from pytest import raises
    booking_in = BookingCreate(user_id=test_user.id, event_id=9999, booking_date=datetime.now())
    with raises(HTTPException):
        create_booking(db, booking_in)
