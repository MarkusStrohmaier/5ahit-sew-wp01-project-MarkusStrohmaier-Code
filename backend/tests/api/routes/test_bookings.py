from fastapi.testclient import TestClient
import pytest
from app.models.userRole import UserRole

BOOKING_BASE_URL = "/api/bookings"

def test_create_booking_as_user(client_with_basic_user: TestClient, test_event_object, test_ticket_id: int):
    booking_data = {
        "event_id": test_event_object.id,
        "ticket_id": test_ticket_id,
        "quantity": 1
    }
    response = client_with_basic_user.post(BOOKING_BASE_URL + "/", json=booking_data)
    assert response.status_code == 200
    assert "booking_number" in response.json()

def test_get_own_booking(client_with_basic_user: TestClient, test_booking_number: int):
    response = client_with_basic_user.get(f"{BOOKING_BASE_URL}/{test_booking_number}")
    assert response.status_code == 200

def test_get_booking_as_admin(client_with_superuser: TestClient, test_booking_number: int):
    response = client_with_superuser.get(f"{BOOKING_BASE_URL}/{test_booking_number}")
    assert response.status_code == 200

def test_get_other_user_booking_forbidden(client_with_basic_user: TestClient, booking_to_delete_other_number: int):
    response = client_with_basic_user.get(f"{BOOKING_BASE_URL}/{booking_to_delete_other_number}")
    assert response.status_code == 403

def test_get_bookings_as_admin(client_with_superuser: TestClient):
    response = client_with_superuser.get(BOOKING_BASE_URL + "/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_bookings_as_user(client_with_basic_user: TestClient):
    response = client_with_basic_user.get(BOOKING_BASE_URL + "/")
    assert response.status_code == 200

def test_update_own_booking(client_with_basic_user: TestClient, test_booking_number: int):
    update_data = {"quantity": 1}
    response = client_with_basic_user.put(f"{BOOKING_BASE_URL}/{test_booking_number}", json=update_data)
    assert response.status_code == 200
    assert "booking_number" in response.json()

def test_update_other_user_booking_forbidden(client_with_basic_user: TestClient, booking_to_delete_other_number: int):
    update_data = {"quantity": 1}
    response = client_with_basic_user.put(f"{BOOKING_BASE_URL}/{booking_to_delete_other_number}", json=update_data)
    assert response.status_code == 403

def test_delete_own_booking(client_with_basic_user: TestClient, booking_to_delete_user_number: int):
    response = client_with_basic_user.delete(f"{BOOKING_BASE_URL}/{booking_to_delete_user_number}")
    assert response.status_code == 200

def test_delete_other_user_booking_forbidden(client_with_basic_user: TestClient, booking_to_delete_other_number: int):
    response = client_with_basic_user.delete(f"{BOOKING_BASE_URL}/{booking_to_delete_other_number}")
    assert response.status_code == 403