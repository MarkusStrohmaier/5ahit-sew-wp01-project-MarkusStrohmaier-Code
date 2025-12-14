from typing import List
from fastapi import APIRouter, HTTPException, status, Query
from app.crud import event as crud
from app.schemas import event as schemas
from app.api.deps import SessionDep, CurrentUser
from app.models.userRole import UserRole

router = APIRouter(tags=["Event"])

@router.post("/", response_model=schemas.Event)
def create_event(db: SessionDep, event: schemas.EventCreate, current_user: CurrentUser):
    if current_user.role not in [UserRole.ADMIN, UserRole.ORGANIZER]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return crud.create_event(db=db, event=event)

@router.get("/{event_id}", response_model=schemas.Event)
def get_event(db: SessionDep, event_id: int):
    return crud.get_event(db=db, event_id=event_id)

@router.get("/", response_model=List[schemas.Event])
def get_events(
    db: SessionDep,
    skip: int = Query(0, ge=0), 
    limit: int = Query(10, le=100), 
    title: str = Query(None), 
    location_id: int = Query(None), 
):
    # Paginierungs- und Suchparameter an die CRUD-Funktion üpbergeben
    return crud.search_events(db=db, skip=skip, limit=limit, title=title, location_id=location_id)

@router.put("/{event_id}", response_model=schemas.Event)
def update_event(db: SessionDep, event_id: int, event: schemas.EventUpdate, current_user: CurrentUser):
    if current_user.role not in [UserRole.ADMIN, UserRole.ORGANIZER]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return crud.update_event(db=db, event_id=event_id, event=event)

@router.delete("/{event_id}", response_model=schemas.Event)
def delete_event(db: SessionDep, event_id: int, current_user: CurrentUser):
    if current_user.role not in [UserRole.ADMIN, UserRole.ORGANIZER]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return crud.delete_event(db=db, event_id=event_id)