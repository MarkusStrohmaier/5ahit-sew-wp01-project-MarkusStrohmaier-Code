from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class BookingBase(BaseModel):

    model_config = ConfigDict(from_attributes=True)
    pass

class BookingCreate(BaseModel):
    event_id: int
    
    booking_date: Optional[datetime] = None 
    
class BookingUpdate(BookingBase):
    event_id: Optional[int] = None
    booking_date: Optional[datetime] = None
class Booking(BookingBase):
    booking_number: int
    user_id: int
    event_id: int
    booking_date: datetime