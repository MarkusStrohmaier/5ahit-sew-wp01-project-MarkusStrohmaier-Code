from sqlalchemy import Column, Integer, String, DateTime, Float, Enum
from app.database.session import Base
from app.models.ticketStatus import TicketStatus

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    seat_num = Column(String(10), index=True, nullable=True)
    price = Column(Float, index=True, nullable=True)
    status = Column(Enum(TicketStatus), nullable=False)
