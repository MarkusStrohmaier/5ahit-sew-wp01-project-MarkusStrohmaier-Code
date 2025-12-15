from fastapi.testclient import TestClient
import pytest
from app.models.ticketStatus import TicketStatus

TICKET_BASE_URL = "/api/tickets"

def test_create_ticket_as_organizer(client_with_organizer: TestClient, test_event_id: int):
    ticket_data = {
        "event_id": test_event_id,
        "name": "General Admission",
        "price": 10.00,
        "total_quantity": 100,
        "status": "CANCELLED"
    }
    response = client_with_organizer.post(TICKET_BASE_URL + "/", json=ticket_data)
    assert response.status_code == 200
    assert "id" in response.json()

def test_create_ticket_forbidden(client_with_basic_user: TestClient, test_event_id: int):
    ticket_data = {
        "event_id": test_event_id,
        "name": "Forbidden Ticket",
        "price": 10.00,
        "total_quantity": 1,
        "status": "CANCELLED" # Fügt fehlendes Feld hinzu
    }
    response = client_with_basic_user.post(TICKET_BASE_URL + "/", json=ticket_data)
    assert response.status_code == 403

def test_get_ticket(client_with_basic_user: TestClient, test_ticket_id: int):
    response = client_with_basic_user.get(f"{TICKET_BASE_URL}/{test_ticket_id}")
    assert response.status_code == 200
    assert response.json()["id"] == test_ticket_id

def test_get_tickets(client_with_basic_user: TestClient):
    response = client_with_basic_user.get(TICKET_BASE_URL + "/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_ticket_as_admin(client_with_superuser: TestClient, test_ticket_id: int):
    update_data = {"price": 15.00}
    response = client_with_superuser.put(f"{TICKET_BASE_URL}/{test_ticket_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["price"] == 15.00

def test_update_ticket_forbidden(client_with_basic_user: TestClient, test_ticket_id: int):
    update_data = {"price": 99.00}
    response = client_with_basic_user.put(f"{TICKET_BASE_URL}/{test_ticket_id}", json=update_data)
    assert response.status_code == 403

def test_delete_ticket_as_organizer(client_with_organizer: TestClient, ticket_to_delete_id: int):
    response = client_with_organizer.delete(f"{TICKET_BASE_URL}/{ticket_to_delete_id}")
    assert response.status_code == 200
    response_get = client_with_organizer.get(f"{TICKET_BASE_URL}/{ticket_to_delete_id}")
    assert response_get.status_code == 404

def test_delete_ticket_forbidden(client_with_basic_user: TestClient, ticket_to_delete_id: int):
    response = client_with_basic_user.delete(f"{TICKET_BASE_URL}/{ticket_to_delete_id}")
    assert response.status_code == 403