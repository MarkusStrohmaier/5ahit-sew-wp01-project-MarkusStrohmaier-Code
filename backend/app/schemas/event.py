from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class EventBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=30)
    date: datetime
    time: Optional[str] = None
    description: Optional[str] = None
    ticket_capacity: Optional[int] = None
    location_id: int

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=30)
    date: Optional[datetime] = None
    time: Optional[str] = None
    description: Optional[str] = None
    ticket_capacity: Optional[int] = None
    location_id: Optional[int] = None

class EventInDBBase(EventBase):
    id: int

    class Config:
        from_attributes = True

class Event(EventInDBBase):
    pass

class EventInDB(EventInDBBase):
    pass
