from pydantic import BaseModel, Field
from typing import Optional

class LocationBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=30)
    address: str = Field(..., min_length=1, max_length=50)
    capacity: Optional[int] = None

class LocationCreate(LocationBase):
    pass

class LocationUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=30)
    address: Optional[str] = Field(None, min_length=1, max_length=50)
    capacity: Optional[int] = None

class LocationInDBBase(LocationBase):
    id: int

    class Config:
        from_attributes = True

class Location(LocationInDBBase):
    pass

class LocationInDB(LocationInDBBase):
    pass
