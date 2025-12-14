from typing import List
from fastapi import APIRouter, HTTPException, status
from app.crud import booking as crud
from app.schemas import booking as schemas
from app.api.deps import SessionDep, CurrentUser
from app.models.userRole import UserRole

router = APIRouter(tags=["Booking"])

@router.post("/", response_model=schemas.Booking)
def create_booking(db: SessionDep, booking: schemas.BookingCreate, current_user: CurrentUser):
    return crud.create_booking(db=db, booking=booking, user_id=current_user.id)

@router.get("/{booking_number}", response_model=schemas.Booking)
def get_booking(db: SessionDep, booking_number: int, current_user: CurrentUser):
    booking = crud.get_booking(db=db, booking_number=booking_number)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    if current_user.role != UserRole.ADMIN and booking.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Not authorized to access this booking"
        )
    return booking

@router.get("/", response_model=List[schemas.Booking])
def get_bookings(db: SessionDep, current_user: CurrentUser):
    if current_user.role == UserRole.ADMIN:
        return crud.get_bookings(db=db)
    
    return crud.get_bookings_by_user(db=db, user_id=current_user.id)

@router.put("/{booking_number}", response_model=schemas.Booking)
def update_booking(db: SessionDep, booking_number: int, booking: schemas.BookingUpdate, current_user: CurrentUser):
    existing_booking = crud.get_booking(db=db, booking_number=booking_number)
    if not existing_booking:
         raise HTTPException(status_code=404, detail="Booking not found")

    if current_user.role != UserRole.ADMIN and existing_booking.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    return crud.update_booking(db=db, booking_number=booking_number, booking=booking)

@router.delete("/{booking_number}", response_model=schemas.Booking)
def delete_booking(db: SessionDep, booking_number: int, current_user: CurrentUser):
    existing_booking = crud.get_booking(db=db, booking_number=booking_number)
    if not existing_booking:
         raise HTTPException(status_code=404, detail="Booking not found")

    if current_user.role != UserRole.ADMIN and existing_booking.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    return crud.delete_booking(db=db, booking_number=booking_number)