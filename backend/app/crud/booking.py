from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.booking import Booking
from app.models.user import User
from app.models.event import Event
from app.schemas.booking import BookingCreate, BookingUpdate


def create_booking(db: Session, booking: BookingCreate):
    user = db.query(User).filter(User.id == booking.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    event = db.query(Event).filter(Event.id == booking.event_id).first()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    db_booking = Booking(
        user_id=booking.user_id,
        event_id=booking.event_id,
        booking_date=booking.booking_date
    )
    db.add(db_booking)
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


def update_booking(db: Session, booking_number: int, booking: BookingUpdate):
    db_booking = db.query(Booking).filter(Booking.booking_number == booking_number).first()
    if not db_booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")

    if booking.user_id:
        user = db.query(User).filter(User.id == booking.user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

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
