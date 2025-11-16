from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class BookingBase(BaseModel):
    user_id: int
    event_id: int
    booking_date: Optional[datetime] = None

class BookingCreate(BookingBase):
    pass

class BookingUpdate(BaseModel):
    user_id: Optional[int] = None
    event_id: Optional[int] = None
    booking_date: Optional[datetime] = None

class BookingInDBBase(BookingBase):
    booking_number: int

    class Config:
        from_attributes = True

class Booking(BookingInDBBase):
    pass

class BookingInDB(BookingInDBBase):
    pass
