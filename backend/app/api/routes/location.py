from typing import List
from fastapi import APIRouter
from app.crud import location as crud
from app.schemas import location as schemas
from app.api.deps import SessionDep

router = APIRouter(tags=["Location"])

@router.post("/", response_model=schemas.Location)
def create_location(db: SessionDep, location: schemas.LocationCreate):
    return crud.create_location(db=db, location=location)

@router.get("/{location_id}", response_model=schemas.Location)
def get_location(db: SessionDep, location_id: int):
    return crud.get_location(db=db, location_id=location_id)

@router.get("/", response_model=List[schemas.Location])
def get_locations(db: SessionDep):
    return crud.get_locations(db=db)

@router.put("/{location_id}", response_model=schemas.Location)
def update_location(db: SessionDep, location_id: int, location: schemas.LocationUpdate):
    return crud.update_location(db=db, location_id=location_id, location=location)

@router.delete("/{location_id}", response_model=schemas.Location)
def delete_location(db: SessionDep, location_id: int):
    return crud.delete_location(db=db, location_id=location_id)
