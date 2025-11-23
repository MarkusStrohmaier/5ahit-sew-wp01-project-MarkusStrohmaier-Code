from fastapi import APIRouter

from app.api.routes import cmd, users, login, booking, event, location, ticket

api_router = APIRouter()
api_router.include_router(cmd.router)
api_router.include_router(users.router)
api_router.include_router(login.router)
api_router.include_router(booking.router)
api_router.include_router(ticket.router, prefix="/bookings")
api_router.include_router(event.router, prefix="/events")
api_router.include_router(location.router, prefix="/locations")
