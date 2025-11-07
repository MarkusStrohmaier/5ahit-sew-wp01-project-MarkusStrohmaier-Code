from app.database.session import Base

class UserRole(Base):
    ADMIN = "ADMIN"
    ORGANIZER = "ORGANIZER"
    VISITOR = "VISITOR"
