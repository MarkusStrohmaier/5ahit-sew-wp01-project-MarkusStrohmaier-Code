from typing import List
from fastapi import APIRouter, HTTPException, status, Query
from app.crud import ticket as crud
from app.schemas import ticket as schemas
from app.api.deps import SessionDep, CurrentUser
from app.models.userRole import UserRole
from app.models.ticketStatus import TicketStatus

router = APIRouter(tags=["Ticket"])

@router.get("/me", response_model=List[schemas.Ticket])
def read_my_tickets(
    db: SessionDep,
    current_user: CurrentUser
):
    return crud.get_tickets_by_user(db=db, user_id=current_user.id)

@router.get("/", response_model=List[schemas.Ticket])
def get_tickets(
    db: SessionDep,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    event_id: int = Query(None),
    status: TicketStatus = Query(None)
):
    return crud.search_tickets(db=db, skip=skip, limit=limit, event_id=event_id, status=status)

@router.get("/{ticket_id}", response_model=schemas.Ticket)
def get_ticket(db: SessionDep, ticket_id: int):
    return crud.get_ticket(db=db, ticket_id=ticket_id)

@router.post("/", response_model=schemas.Ticket)
def create_ticket(db: SessionDep, ticket: schemas.TicketCreate, current_user: CurrentUser):
    if current_user.role not in [UserRole.ADMIN, UserRole.ORGANIZER]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return crud.create_ticket(db=db, ticket=ticket)

@router.put("/{ticket_id}", response_model=schemas.Ticket)
def update_ticket(db: SessionDep, ticket_id: int, ticket: schemas.TicketUpdate, current_user: CurrentUser):
    if current_user.role not in [UserRole.ADMIN, UserRole.ORGANIZER]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return crud.update_ticket(db=db, ticket_id=ticket_id, ticket=ticket)

@router.delete("/{ticket_id}", response_model=schemas.Ticket)
def delete_ticket(db: SessionDep, ticket_id: int, current_user: CurrentUser):
    if current_user.role not in [UserRole.ADMIN, UserRole.ORGANIZER]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return crud.delete_ticket(db=db, ticket_id=ticket_id)