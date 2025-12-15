from fastapi.testclient import TestClient
import pytest

LOCATION_BASE_URL = "/api/locations"

def test_create_location_as_admin(client_with_superuser: TestClient):
    location_data = {"name": "Test Location Admin", "address": "123 Admin St"}
    response = client_with_superuser.post(LOCATION_BASE_URL + "/", json=location_data)
    assert response.status_code == 200
    assert response.json()["name"] == location_data["name"]

def test_create_location_as_organizer(client_with_organizer: TestClient):
    location_data = {"name": "Test Location Organizer", "address": "456 Org Ave"}
    response = client_with_organizer.post(LOCATION_BASE_URL + "/", json=location_data)
    assert response.status_code == 200

def test_create_location_forbidden(client_with_basic_user: TestClient):
    location_data = {"name": "Forbidden Location", "address": "999 No Way"}
    response = client_with_basic_user.post(LOCATION_BASE_URL + "/", json=location_data)
    assert response.status_code == 403

def test_get_location(client_with_basic_user: TestClient, test_location: object):
    response = client_with_basic_user.get(f"{LOCATION_BASE_URL}/{test_location.id}")
    assert response.status_code == 200
    assert response.json()["id"] == test_location.id

def test_get_locations(client_with_basic_user: TestClient):
    response = client_with_basic_user.get(LOCATION_BASE_URL + "/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_location_as_admin(client_with_superuser: TestClient, test_location: object):
    update_data = {"name": "Updated Location Name"}
    response = client_with_superuser.put(f"{LOCATION_BASE_URL}/{test_location.id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["name"] == update_data["name"]

def test_update_location_forbidden(client_with_basic_user: TestClient, test_location: object):
    update_data = {"name": "Attempted Update"}
    response = client_with_basic_user.put(f"{LOCATION_BASE_URL}/{test_location.id}", json=update_data)
    assert response.status_code == 403

def test_delete_location_as_admin(client_with_superuser: TestClient, location_to_delete: object):
    response = client_with_superuser.delete(f"{LOCATION_BASE_URL}/{location_to_delete.id}")
    assert response.status_code == 200
    response_get = client_with_superuser.get(f"{LOCATION_BASE_URL}/{location_to_delete.id}")
    assert response_get.status_code == 404

def test_delete_location_forbidden(client_with_basic_user: TestClient, location_to_delete: object):
    response = client_with_basic_user.delete(f"{LOCATION_BASE_URL}/{location_to_delete.id}")
    assert response.status_code == 403