import pytest
from datetime import datetime
from sqlalchemy.orm import Session
from app.crud.ticket import create_ticket, get_ticket, get_tickets, update_ticket, delete_ticket
from app.models.ticket import Ticket
from app.models.event import Event
from app.models.booking import Booking
from app.schemas.ticket import TicketCreate, TicketUpdate
from app.models.ticketStatus import TicketStatus

@pytest.fixture
def test_event(db: Session):
    event = Event(
        title="Test Event",
        date=datetime.now(),
        ticket_capacity=100
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

@pytest.fixture
def test_booking(db: Session, test_event: Event):
    booking = Booking(
        user_id=1,
        event_id=test_event.id
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking

def test_create_ticket(db: Session, test_event: Event, test_booking: Booking):
    ticket_in = TicketCreate(
        seat_num="A1",
        price=50.0,
        status=TicketStatus.SOLD,
        event_id=test_event.id,
        booking_id=test_booking.booking_number
    )
    ticket: Ticket = create_ticket(db, ticket_in)
    assert isinstance(ticket.id, int)
    assert ticket.seat_num == "A1"
    assert ticket.price == 50.0
    assert ticket.status == TicketStatus.SOLD
    assert ticket.event_id == test_event.id
    assert ticket.booking_id == test_booking.booking_number

def test_get_ticket(db: Session, test_event: Event, test_booking: Booking):
    ticket_in = TicketCreate(
        seat_num="B2",
        price=60.0,
        status=TicketStatus.SOLD,
        event_id=test_event.id,
        booking_id=test_booking.booking_number
    )
    ticket = create_ticket(db, ticket_in)
    fetched = get_ticket(db, ticket.id)
    assert fetched.id == ticket.id
    assert fetched.seat_num == "B2"

def test_get_tickets(db: Session, test_event: Event, test_booking: Booking):
    t1 = create_ticket(db, TicketCreate(seat_num="C1", price=30, status=TicketStatus.SOLD, event_id=test_event.id, booking_id=test_booking.booking_number))
    t2 = create_ticket(db, TicketCreate(seat_num="C2", price=35, status=TicketStatus.CANCELLED, event_id=test_event.id, booking_id=test_booking.booking_number))
    all_tickets = get_tickets(db)
    ids = [t.id for t in all_tickets]
    assert t1.id in ids
    assert t2.id in ids

def test_update_ticket(db: Session, test_event: Event, test_booking: Booking):
    ticket = create_ticket(db, TicketCreate(seat_num="D1", price=40, status=TicketStatus.SOLD, event_id=test_event.id, booking_id=test_booking.booking_number))
    update_data = TicketUpdate(seat_num="D2", price=45, status=TicketStatus.CANCELLED)
    updated = update_ticket(db, ticket.id, update_data)
    assert updated.seat_num == "D2"
    assert updated.price == 45
    assert updated.status == TicketStatus.CANCELLED

def test_delete_ticket(db: Session, test_event: Event, test_booking: Booking):
    ticket = create_ticket(db, TicketCreate(seat_num="E1", price=70, status=TicketStatus.SOLD, event_id=test_event.id, booking_id=test_booking.booking_number))
    deleted = delete_ticket(db, ticket.id)
    assert deleted.id == ticket.id
    from fastapi import HTTPException
    import pytest
    with pytest.raises(HTTPException):
        get_ticket(db, ticket.id)

def test_create_ticket_with_invalid_event(db: Session, test_booking: Booking):
    ticket_in = TicketCreate(
        seat_num="F1",
        price=50,
        status=TicketStatus.SOLD,
        event_id=99999,
        booking_id=test_booking.booking_number
    )
    import pytest
    from fastapi import HTTPException
    with pytest.raises(HTTPException):
        create_ticket(db, ticket_in)

def test_create_ticket_with_invalid_booking(db: Session, test_event: Event):
    ticket_in = TicketCreate(
        seat_num="G1",
        price=50,
        status=TicketStatus.SOLD,
        event_id=test_event.id,
        booking_id=99999
    )
    import pytest
    from fastapi import HTTPException
    with pytest.raises(HTTPException):
        create_ticket(db, ticket_in)
