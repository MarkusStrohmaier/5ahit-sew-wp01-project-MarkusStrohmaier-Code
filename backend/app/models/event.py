from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(30), nullable=False)
    date = Column(DateTime, nullable=False)
    time = Column(String, nullable=True)
    description = Column(String(50), nullable=True)

    location_id = Column(Integer, ForeignKey("locations.id"))
    ticket_capacity = Column(Integer, index=True, nullable=True)

    location = relationship("Location", back_populates="events")
    tickets = relationship("Ticket", back_populates="event", cascade="all, delete-orphan")
    bookings = relationship("Booking", back_populates="event", cascade="all, delete-orphan")
