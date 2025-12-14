from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from app.database.session import Base
from datetime import datetime
from app.models.userRole import UserRole 

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(15), unique=True, index=True, nullable=False)
    email = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    role = Column(
        Enum(UserRole), 
        default=UserRole.VISITOR, 
        nullable=False
    )
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)

    bookings = relationship("Booking", back_populates="user", cascade="all, delete-orphan")
