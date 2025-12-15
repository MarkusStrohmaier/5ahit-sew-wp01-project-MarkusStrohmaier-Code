import pytest
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException
from starlette import status
from sqlalchemy import select
import uuid

from app.crud.booking import create_booking, get_booking, search_bookings, update_booking, delete_booking
from app.crud.ticket import create_ticket
from app.models.booking import Booking
from app.models.user import User
from app.models.event import Event
from app.models.ticket import Ticket
from app.models.ticketStatus import TicketStatus
from app.schemas.booking import BookingCreate, BookingUpdate
from app.schemas.ticket import TicketCreate

@pytest.fixture
def test_user(db: Session):
    unique_username = f"bookuser_{uuid.uuid4().hex[:8]}"
    user = User(username=unique_username, email=f"{unique_username}@example.com", hashed_password="hashedpw")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def test_event(db: Session):
    event = Event(title="Test Booking Event", date=datetime.now(), ticket_capacity=100)
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

@pytest.fixture
def test_ticket_type(db: Session, test_event: Event):
    ticket_in = TicketCreate(
        event_id=test_event.id,
        seat_num="GA",
        price=10.00,
        total_quantity=10, 
        status=TicketStatus.CANCELLED
    )
    ticket = create_ticket(db, ticket_in)
    return ticket

@pytest.fixture
def test_booking(db: Session, test_user: User, test_event: Event, test_ticket_type: Ticket): 
    booking_in = BookingCreate(
        event_id=test_event.id, 
        ticket_id=test_ticket_type.id, 
        quantity=1,
        booking_date=datetime.now()
    ) 
    booking = create_booking(db, booking_in, user_id=test_user.id)
    return booking

def test_create_booking(db: Session, test_user: User, test_event: Event, test_ticket_type: Ticket):
    booking_in = BookingCreate(
        event_id=test_event.id, 
        ticket_id=test_ticket_type.id, 
        quantity=1,
        booking_date=datetime.now()
    )
    booking = create_booking(db, booking_in, user_id=test_user.id)

    assert isinstance(booking.booking_number, int)
    assert booking.user_id == test_user.id
    assert booking.event_id == test_event.id

def test_get_booking(db: Session, test_booking: Booking):
    fetched = get_booking(db, test_booking.booking_number)
    assert fetched.booking_number == test_booking.booking_number
    assert fetched.user_id == test_booking.user_id

def test_get_bookings(db: Session, test_booking: Booking):
    all_bookings = search_bookings(db, skip=0, limit=100)
    booking_numbers = [b.booking_number for b in all_bookings]
    assert test_booking.booking_number in booking_numbers

def test_update_booking(db: Session, test_booking: Booking, test_event: Event, test_user: User):
    update_data = BookingUpdate(event_id=test_event.id)
    updated = update_booking(db, test_booking.booking_number, update_data)
    assert updated.event_id == test_event.id

def test_delete_booking(db: Session, test_booking: Booking):
    deleted = delete_booking(db, test_booking.booking_number)
    assert deleted.booking_number == test_booking.booking_number

    with pytest.raises(HTTPException):
        get_booking(db, test_booking.booking_number)


def test_create_booking_invalid_event(db: Session, test_user: User, test_ticket_type: Ticket):
    booking_in = BookingCreate(
        event_id=9999, 
        ticket_id=test_ticket_type.id, 
        quantity=1,
        booking_date=datetime.now()
    )
    with pytest.raises(HTTPException):
        create_booking(db, booking_in, user_id=test_user.id)