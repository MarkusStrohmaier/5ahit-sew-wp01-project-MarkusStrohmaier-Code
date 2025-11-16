from sqlalchemy.orm import Session
from app.models.user import User
from app.models.location import Location
from app.models.event import Event
from datetime import datetime

def init_db(db: Session) -> None:
    """Called by initial_data.py to create seed records."""

    # verhindert, dass Seeds mehrfach ausgeführt werden
    if db.query(User).first():
        print("Seed-Daten bereits vorhanden.")
        return

    # USER
    admin = User(
        username="admin",
        email="admin@example.com",
        hashed_password="hashed_pw_123",
        is_superuser=True
    )

    # LOCATION
    loc = Location(
        name="Haupt Halle",
        address="Musterstraße 1",
        capacity=1500
    )

    # EVENT
    event = Event(
        title="Opening Night",
        date=datetime(2025, 5, 20),
        time="20:00",
        description="Eröffnungsfeier",
        location=loc,
        ticket_capacity=1500
    )

    db.add(admin)
    db.add(loc)
    db.add(event)
    db.commit()

    print("Seed-Daten erfolgreich eingefügt.")
