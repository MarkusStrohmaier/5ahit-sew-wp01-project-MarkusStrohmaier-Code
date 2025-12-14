from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.ticket import Ticket
from app.models.event import Event
from app.models.booking import Booking
from app.schemas.ticket import TicketCreate, TicketUpdate
from app.models.ticketStatus import TicketStatus


def create_ticket(db: Session, ticket: TicketCreate):
    event = db.query(Event).filter(Event.id == ticket.event_id).first()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    booking_number = getattr(ticket, "booking_id", None)
    if booking_number is not None:
        booking = db.query(Booking).filter(Booking.booking_number == booking_number).first()
        if not booking:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")

    db_ticket = Ticket(
        seat_num=ticket.seat_num,
        price=ticket.price,
        status=ticket.status,
        event_id=ticket.event_id,
        booking_id=booking_number
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket


def get_ticket(db: Session, ticket_id: int):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
    return ticket


def get_tickets(db: Session):
    return db.query(Ticket).all()


def update_ticket(db: Session, ticket_id: int, ticket: TicketUpdate):
    db_ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not db_ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")

    if ticket.event_id is not None:
        event = db.query(Event).filter(Event.id == ticket.event_id).first()
        if not event:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    booking_number = getattr(ticket, "booking_id", None)
    if booking_number is not None:
        booking = db.query(Booking).filter(Booking.booking_number == booking_number).first()
        if not booking:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")

    for key, value in ticket.dict(exclude_unset=True).items():
        setattr(db_ticket, key, value)

    db.commit()
    db.refresh(db_ticket)
    return db_ticket


def delete_ticket(db: Session, ticket_id: int):
    db_ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not db_ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")

    db.delete(db_ticket)
    db.commit()
    return db_ticket

def search_tickets(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    event_id: int = None,
    status: TicketStatus = None
):
    query = db.query(Ticket)
    
    if event_id is not None:
        query = query.filter(Ticket.event_id == event_id)
        
    if status is not None:
        query = query.filter(Ticket.status == status)
        
    return query.offset(skip).limit(limit).all()