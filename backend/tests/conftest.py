import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient
from app.database.session import Base
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.userRole import UserRole
from app.models.location import Location
from app.models.event import Event
from app.models.ticket import Ticket
from app.models.ticketStatus import TicketStatus
from app.models.booking import Booking
from app.main import app
from datetime import datetime
from passlib.context import CryptContext
from typing import Generator
import uuid

SQLALCHEMY_DATABASE_URL = "sqlite:///test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

@pytest.fixture(scope="function")
def db() -> Generator[Session, None, None]:
    Base.metadata.create_all(bind=engine) 
    session = TestingSessionLocal()
    try:
        yield session  
    finally:
        session.rollback()
        session.close()
        Base.metadata.drop_all(bind=engine) 

@pytest.fixture(scope="function")
def client(db: Session) -> TestClient:
    def override_get_db():
        yield db
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

def create_test_user(db: Session, username_prefix: str, role: UserRole) -> User:
    unique_username = f"{username_prefix}_{uuid.uuid4().hex[:6]}"
    user = User(
        username=unique_username,
        email=f"{unique_username}@example.com",
        hashed_password=hash_password("Kennwort1"),
        role=role,
        created_at=datetime.now()
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    db.expunge(user)
    return user

@pytest.fixture
def test_superuser(db: Session) -> User:
    return create_test_user(db, "admin", UserRole.ADMIN)

@pytest.fixture
def test_organizer(db: Session) -> User:
    return create_test_user(db, "organizer", UserRole.ORGANIZER)

@pytest.fixture
def test_basic_user(db: Session) -> User:
    return create_test_user(db, "basic", UserRole.VISITOR)

@pytest.fixture
def client_with_superuser(client: TestClient, test_superuser: User) -> TestClient:
    def override_get_current_user():
        return test_superuser 
    app.dependency_overrides[get_current_user] = override_get_current_user
    return client

@pytest.fixture
def client_with_organizer(client: TestClient, test_organizer: User) -> TestClient:
    def override_get_current_user():
        return test_organizer 
    app.dependency_overrides[get_current_user] = override_get_current_user
    return client

@pytest.fixture
def client_with_basic_user(client: TestClient, test_basic_user: User) -> TestClient:
    def override_get_current_user():
        return test_basic_user 
    app.dependency_overrides[get_current_user] = override_get_current_user
    return client

@pytest.fixture
def test_user_credentials(test_basic_user: User) -> dict:
    return {"username": test_basic_user.username, "password": "Kennwort1"}

@pytest.fixture
def test_location(db: Session) -> Location:
    location = Location(name="Test Hall", address="123 Test St", capacity=200)
    db.add(location)
    db.commit()
    db.refresh(location)
    return location

@pytest.fixture
def test_event_object(db: Session, test_location: Location, test_organizer: User) -> Event:
    event = Event(
        title="API Test Event",
        date=datetime.now(),
        ticket_capacity=100,
        location_id=test_location.id,
    )
    event.organizer_id = test_organizer.id
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

@pytest.fixture
def event_to_delete(db: Session, test_location: Location, test_organizer: User) -> Event:
    event = Event(
        title="Event to Delete",
        date=datetime.now(),
        ticket_capacity=50,
        location_id=test_location.id,
    )
    event.organizer_id = test_organizer.id
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

@pytest.fixture
def location_to_delete(db: Session) -> Location:
    location = Location(name="Location to Delete", address="444 Del St", capacity=10)
    db.add(location)
    db.commit()
    db.refresh(location)
    return location

@pytest.fixture
def test_ticket_object(db: Session, test_event_object: Event) -> Ticket:
    # Status auf CANCELLED gesetzt, um Buchungen im Test zu ermöglichen
    ticket = Ticket(
        event_id=test_event_object.id,
        seat_num="GA",
        price=10.0,
        status=TicketStatus.CANCELLED 
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket

@pytest.fixture
def test_event_id(test_event_object: Event) -> int:
    return test_event_object.id

@pytest.fixture
def test_ticket_id(test_ticket_object: Ticket) -> int:
    return test_ticket_object.id

@pytest.fixture
def ticket_to_delete_id(db: Session, test_event_object: Event) -> int:
    ticket = Ticket(event_id=test_event_object.id, seat_num="X1", price=10.0, status=TicketStatus.SOLD)
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket.id

@pytest.fixture
def test_booking_obj(db: Session, test_basic_user: User, test_event_object: Event, test_ticket_object: Ticket) -> Booking:
    # ticket_id entfernt, um TypeError zu vermeiden
    booking = Booking(
        user_id=test_basic_user.id,
        event_id=test_event_object.id,
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking

@pytest.fixture
def test_booking_number(test_booking_obj: Booking) -> int:
    return test_booking_obj.booking_number

@pytest.fixture
def booking_to_delete_user_number(db: Session, test_basic_user: User, test_event_object: Event, test_ticket_object: Ticket) -> int:
    booking = Booking(
        user_id=test_basic_user.id,
        event_id=test_event_object.id,
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking.booking_number

@pytest.fixture
def booking_to_delete_other_number(db: Session, test_superuser: User, test_event_object: Event, test_ticket_object: Ticket) -> int:
    booking = Booking(
        user_id=test_superuser.id,
        event_id=test_event_object.id,
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking.booking_number