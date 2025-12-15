from fastapi.testclient import TestClient
import pytest
from datetime import datetime

EVENT_BASE_URL = "/api/events"

def test_create_event_as_admin(client_with_superuser: TestClient, test_location: object):
    event_data = {
        "title": "Admin Created Event",
        "description": "Test description",
        "date": "2026-01-01T10:00:00",
        "location_id": test_location.id,
        # organizer_id ENTFERNT
    }
    response = client_with_superuser.post(EVENT_BASE_URL + "/", json=event_data)
    assert response.status_code == 200
    assert response.json()["title"] == event_data["title"]

def test_create_event_forbidden(client_with_basic_user: TestClient, test_location: object):
    event_data = {
        "title": "Forbidden Event",
        "description": "No access",
        "date": "2026-01-01T10:00:00",
        "location_id": test_location.id,
        # organizer_id ENTFERNT
    }
    response = client_with_basic_user.post(EVENT_BASE_URL + "/", json=event_data)
    assert response.status_code == 403

def test_get_event(client_with_basic_user: TestClient, test_event_id: int):
    response = client_with_basic_user.get(f"{EVENT_BASE_URL}/{test_event_id}")
    assert response.status_code == 200
    assert response.json()["id"] == test_event_id

def test_get_events(client_with_basic_user: TestClient):
    response = client_with_basic_user.get(EVENT_BASE_URL + "/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_event_as_organizer(client_with_organizer: TestClient, test_event_id: int):
    update_data = {"title": "Updated Event Title"}
    response = client_with_organizer.put(f"{EVENT_BASE_URL}/{test_event_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["title"] == update_data["title"]

def test_update_event_forbidden(client_with_basic_user: TestClient, test_event_id: int):
    update_data = {"title": "Attempted Update"}
    response = client_with_basic_user.put(f"{EVENT_BASE_URL}/{test_event_id}", json=update_data)
    assert response.status_code == 403

def test_delete_event_as_admin(client_with_superuser: TestClient, event_to_delete: object):
    response = client_with_superuser.delete(f"{EVENT_BASE_URL}/{event_to_delete.id}")
    assert response.status_code == 200
    response_get = client_with_superuser.get(f"{EVENT_BASE_URL}/{event_to_delete.id}")
    assert response_get.status_code == 404

def test_delete_event_forbidden(client_with_basic_user: TestClient, event_to_delete: object):
    response = client_with_basic_user.delete(f"{EVENT_BASE_URL}/{event_to_delete.id}")
    assert response.status_code == 403