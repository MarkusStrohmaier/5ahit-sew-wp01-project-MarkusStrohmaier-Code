from sqlalchemy import Column, DateTime, Integer, String
from app.database.session import Base
from datetime import datetime

class Booking(Base):
    booking_number = Column(Integer, index=True, primary_key=True)
    booking_date = Column(DateTime, index=True, default=datetime.utcnow)
