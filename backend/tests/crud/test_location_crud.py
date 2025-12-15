import pytest
from sqlalchemy.orm import Session
from app.crud.location import create_location, get_location, get_locations, update_location, delete_location
from app.models.location import Location
from app.schemas.location import LocationCreate, LocationUpdate
from fastapi import HTTPException

@pytest.fixture
def test_location(db: Session):
    location_in = LocationCreate(
        name="Test Hall",
        address="123 Test Street",
        capacity=200
    )
    location = create_location(db, location_in) 
    return location

def test_create_location(db: Session):
    location_in = LocationCreate(
        name="Main Hall",
        address="456 Main Street",
        capacity=300
    )
    location: Location = create_location(db, location_in)
    assert isinstance(location.id, int)
    assert location.name == "Main Hall"
    assert location.address == "456 Main Street"
    assert location.capacity == 300

def test_get_location(db: Session, test_location: Location):
    fetched = get_location(db, test_location.id)
    assert fetched.id == test_location.id
    assert fetched.name == test_location.name

def test_get_locations(db: Session, test_location: Location):
    all_locations = get_locations(db)
    ids = [loc.id for loc in all_locations]
    assert test_location.id in ids

def test_update_location(db: Session, test_location: Location):
    update_data = LocationUpdate(name="Updated Hall", capacity=250)
    updated = update_location(db, test_location.id, update_data)
    assert updated.name == "Updated Hall"
    assert updated.capacity == 250
    assert updated.address == test_location.address

def test_delete_location(db: Session, test_location: Location):
    deleted = delete_location(db, test_location.id)
    assert deleted.id == test_location.id
    with pytest.raises(HTTPException):
        get_location(db, test_location.id)

def test_get_location_not_found(db: Session):
    with pytest.raises(HTTPException):
        get_location(db, 99999)

def test_update_location_not_found(db: Session):
    update_data = LocationUpdate(name="Nonexistent")
    with pytest.raises(HTTPException):
        update_location(db, 99999, update_data)

def test_delete_location_not_found(db: Session):
    with pytest.raises(HTTPException):
        delete_location(db, 99999)