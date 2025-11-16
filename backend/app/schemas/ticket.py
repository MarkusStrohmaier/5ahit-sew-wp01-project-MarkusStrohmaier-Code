from pydantic import BaseModel
from typing import Optional

from app.models.ticketStatus import TicketStatus

class TicketBase(BaseModel):
    seat_num: Optional[str] = None
    price: Optional[float] = None
    status: TicketStatus
    event_id: int
    booking_id: Optional[int] = None

class TicketCreate(TicketBase):
    pass

class TicketUpdate(BaseModel):
    seat_num: Optional[str] = None
    price: Optional[float] = None
    status: Optional[TicketStatus] = None
    event_id: Optional[int] = None
    booking_id: Optional[int] = None

class TicketInDBBase(TicketBase):
    id: int

    class Config:
        from_attributes = True

class Ticket(TicketInDBBase):
    pass

class TicketInDB(TicketInDBBase):
    pass
