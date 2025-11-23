from typing import List
from fastapi import APIRouter
from app.crud import ticket as crud
from app.schemas import ticket as schemas
from app.api.deps import SessionDep

router = APIRouter(tags=["Ticket"])

@router.post("/", response_model=schemas.Ticket)
def create_ticket(db: SessionDep, ticket: schemas.TicketCreate):
    return crud.create_ticket(db=db, ticket=ticket)

@router.get("/{ticket_id}", response_model=schemas.Ticket)
def get_ticket(db: SessionDep, ticket_id: int):
    return crud.get_ticket(db=db, ticket_id=ticket_id)

@router.get("/", response_model=List[schemas.Ticket])
def get_tickets(db: SessionDep):
    return crud.get_tickets(db=db)

@router.put("/{ticket_id}", response_model=schemas.Ticket)
def update_ticket(db: SessionDep, ticket_id: int, ticket: schemas.TicketUpdate):
    return crud.update_ticket(db=db, ticket_id=ticket_id, ticket=ticket)

@router.delete("/{ticket_id}", response_model=schemas.Ticket)
def delete_ticket(db: SessionDep, ticket_id: int):
    return crud.delete_ticket(db=db, ticket_id=ticket_id)
