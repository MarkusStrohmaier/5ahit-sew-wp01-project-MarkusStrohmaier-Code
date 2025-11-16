from sqlalchemy import Column, Integer, String, Float, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base
from app.models.ticketStatus import TicketStatus

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    seat_num = Column(String(10), index=True, nullable=True)
    price = Column(Float, nullable=True)
    status = Column(Enum(TicketStatus), nullable=False)

    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    booking_id = Column(Integer, ForeignKey("bookings.booking_number"))

    event = relationship("Event", back_populates="tickets")
    booking = relationship("Booking", back_populates="tickets")
