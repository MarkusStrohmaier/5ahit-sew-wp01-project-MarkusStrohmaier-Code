from typing import List
from fastapi import APIRouter, HTTPException, status, Query
from app.crud import location as crud
from app.schemas import location as schemas
from app.api.deps import SessionDep, CurrentUser
from app.models.userRole import UserRole

router = APIRouter(tags=["Location"])

@router.post("/", response_model=schemas.Location)
def create_location(db: SessionDep, location: schemas.LocationCreate, current_user: CurrentUser):
    if current_user.role not in [UserRole.ADMIN, UserRole.ORGANIZER]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return crud.create_location(db=db, location=location)

@router.get("/{location_id}", response_model=schemas.Location)
def get_location(db: SessionDep, location_id: int):
    return crud.get_location(db=db, location_id=location_id)

@router.get("/", response_model=List[schemas.Location])
def get_locations(
    db: SessionDep,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    name: str = Query(None)
):
    return crud.search_locations(db=db, skip=skip, limit=limit, name=name)

@router.put("/{location_id}", response_model=schemas.Location)
def update_location(db: SessionDep, location_id: int, location: schemas.LocationUpdate, current_user: CurrentUser):
    if current_user.role not in [UserRole.ADMIN, UserRole.ORGANIZER]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return crud.update_location(db=db, location_id=location_id, location=location)

@router.delete("/{location_id}", response_model=schemas.Location)
def delete_location(db: SessionDep, location_id: int, current_user: CurrentUser):
    if current_user.role not in [UserRole.ADMIN, UserRole.ORGANIZER]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return crud.delete_location(db=db, location_id=location_id)