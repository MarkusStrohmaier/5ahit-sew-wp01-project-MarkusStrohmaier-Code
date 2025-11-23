from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.location import Location
from app.schemas.location import LocationCreate, LocationUpdate


def create_location(db: Session, location: LocationCreate):
    db_location = Location(
        name=location.name,
        address=location.address,
        capacity=location.capacity
    )
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location


def get_location(db: Session, location_id: int):
    location = db.query(Location).filter(Location.id == location_id).first()
    if not location:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location not found")
    return location


def get_locations(db: Session):
    return db.query(Location).all()


def update_location(db: Session, location_id: int, location: LocationUpdate):
    db_location = db.query(Location).filter(Location.id == location_id).first()
    if not db_location:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location not found")

    for key, value in location.dict(exclude_unset=True).items():
        setattr(db_location, key, value)

    db.commit()
    db.refresh(db_location)
    return db_location


def delete_location(db: Session, location_id: int):
    db_location = db.query(Location).filter(Location.id == location_id).first()
    if not db_location:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location not found")

    db.delete(db_location)
    db.commit()
    return db_location
