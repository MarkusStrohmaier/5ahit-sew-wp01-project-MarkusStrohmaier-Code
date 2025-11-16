from app.database.session import Base

class TicketStatus(Base):
    SOLD = "SOLD"
    CANCELLED = "CANCELLED"
