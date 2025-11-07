from app.database.session import Base

class TicketStatus(Base):
    AVAILABLE = "AVAILABLE"
    SOLD = "SOLD"
    CANCELLED = "CANCELLED"
