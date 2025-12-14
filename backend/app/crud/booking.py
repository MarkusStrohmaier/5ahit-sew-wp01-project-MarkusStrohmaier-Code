from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.booking import Booking
from app.models.event import Event
from app.models.ticket import Ticket
from app.models.ticketStatus import TicketStatus
from app.schemas.booking import BookingCreate, BookingUpdate


def create_booking(db: Session, booking: BookingCreate, user_id: int):
    
    ticket_to_book_stmt = (
        select(Ticket)
        .filter(Ticket.event_id == booking.event_id)
        .filter(Ticket.status != TicketStatus.SOLD)
        .limit(1)
        .with_for_update(skip_locked=True) 
    )
    
    ticket_to_book = db.scalar(ticket_to_book_stmt)

    if not ticket_to_book:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No available tickets found for this event.")

    db_booking = Booking(
        user_id=user_id, 
        event_id=booking.event_id,
        booking_date=booking.booking_date
    )
    db.add(db_booking)
    
    ticket_to_book.status = TicketStatus.SOLD
    ticket_to_book.booking = db_booking
    
    db.add(ticket_to_book)
    
    db.commit() 
    db.refresh(db_booking)
    return db_booking


def get_booking(db: Session, booking_number: int):
    booking = db.query(Booking).filter(Booking.booking_number == booking_number).first()
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    return booking


def get_bookings(db: Session):
    return db.query(Booking).all()

def get_bookings_by_user(db: Session, user_id: int):
    return db.query(Booking).filter(Booking.user_id == user_id).all()

def get_bookings_by_organizer(db: Session, organizer_id: int):
    return (
        db.query(Booking)
        .join(Event)
        .all()
    )


def update_booking(db: Session, booking_number: int, booking: BookingUpdate):
    db_booking = db.query(Booking).filter(Booking.booking_number == booking_number).first()
    if not db_booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")

    if booking.event_id:
        event = db.query(Event).filter(Event.id == booking.event_id).first()
        if not event:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    for key, value in booking.dict(exclude_unset=True).items():
        setattr(db_booking, key, value)

    db.commit()
    db.refresh(db_booking)
    return db_booking


def delete_booking(db: Session, booking_number: int):
    db_booking = db.query(Booking).filter(Booking.booking_number == booking_number).first()
    if not db_booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")

    db.delete(db_booking)
    db.commit()
    return db_booking