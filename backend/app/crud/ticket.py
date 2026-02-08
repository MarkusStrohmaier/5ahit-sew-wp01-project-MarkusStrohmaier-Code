from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.ticket import Ticket
from app.models.event import Event
from app.models.booking import Booking
from app.schemas.ticket import TicketCreate, TicketUpdate
from app.models.ticketStatus import TicketStatus

def get_tickets_by_user(db: Session, user_id: int):
    return (
        db.query(Ticket)
        .join(Booking, Ticket.booking_id == Booking.booking_number)
        .filter(Booking.user_id == user_id)
        .all()
    )

def create_ticket(db: Session, ticket: TicketCreate):
    event = db.query(Event).filter(Event.id == ticket.event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    if event.ticket_capacity is not None:
        ticket_count = db.query(Ticket).filter(Ticket.event_id == event.id).count()
        if ticket_count >= event.ticket_capacity:
            raise HTTPException(status_code=400, detail="Capacity reached")

    db_ticket = Ticket(
        seat_num=ticket.seat_num,
        price=ticket.price,
        status=ticket.status,
        event_id=ticket.event_id,
        booking_id=ticket.booking_id
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

def get_ticket(db: Session, ticket_id: int):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

def search_tickets(db: Session, skip: int = 0, limit: int = 10, event_id: int = None, status: TicketStatus = None):
    query = db.query(Ticket)
    if event_id:
        query = query.filter(Ticket.event_id == event_id)
    if status:
        query = query.filter(Ticket.status == status)
    return query.offset(skip).limit(limit).all()

def update_ticket(db: Session, ticket_id: int, ticket: TicketUpdate):
    db_ticket = get_ticket(db, ticket_id)
    for key, value in ticket.dict(exclude_unset=True).items():
        setattr(db_ticket, key, value)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

def delete_ticket(db: Session, ticket_id: int):
    db_ticket = get_ticket(db, ticket_id)
    db.delete(db_ticket)
    db.commit()
    return db_ticket