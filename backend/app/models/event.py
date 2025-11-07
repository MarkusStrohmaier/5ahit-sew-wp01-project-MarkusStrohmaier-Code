from sqlalchemy import Column, Integer, String, DateTime
from app.database.session import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(30), index=True, nullable=False)
    date = Column(DateTime, nullable=False)
    time = Column(String, index=True, nullable=True)
    description = Column(String(50), nullable=True)
    ticket_capacity = Column(Integer, index=True, nullable=True)
