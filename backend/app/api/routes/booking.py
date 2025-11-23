from typing import List
from fastapi import APIRouter
from app.crud import booking as crud
from app.schemas import booking as schemas
from app.api.deps import SessionDep

router = APIRouter(tags=["Booking"])

@router.post("/", response_model=schemas.Booking)
def create_booking(db: SessionDep, booking: schemas.BookingCreate):
    return crud.create_booking(db=db, booking=booking)

@router.get("/{booking_number}", response_model=schemas.Booking)
def get_booking(db: SessionDep, booking_number: int):
    return crud.get_booking(db=db, booking_number=booking_number)

@router.get("/", response_model=List[schemas.Booking])
def get_bookings(db: SessionDep):
    return crud.get_bookings(db=db)

@router.put("/{booking_number}", response_model=schemas.Booking)
def update_booking(db: SessionDep, booking_number: int, booking: schemas.BookingUpdate):
    return crud.update_booking(db=db, booking_number=booking_number, booking=booking)

@router.delete("/{booking_number}", response_model=schemas.Booking)
def delete_booking(db: SessionDep, booking_number: int):
    return crud.delete_booking(db=db, booking_number=booking_number)
