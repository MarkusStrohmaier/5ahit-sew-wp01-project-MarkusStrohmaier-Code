from app.database.session import Base
from enum import Enum

class UserRole(Enum):
    ADMIN = "ADMIN"
    ORGANIZER = "ORGANIZER"
    VISITOR = "VISITOR"
