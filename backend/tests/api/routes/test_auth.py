from fastapi.testclient import TestClient
import pytest

AUTH_BASE_URL = "/api/login"

def test_login_incorrect_password(client: TestClient, test_user_credentials: dict):
    form_data = {
        "username": test_user_credentials["username"],
        "password": "wrongpassword"
    }
    response = client.post(AUTH_BASE_URL + "/login", data=form_data)
    assert response.status_code == 400

def test_test_access_token_success(client_with_basic_user: TestClient):
    response = client_with_basic_user.post(AUTH_BASE_URL + "/me")
    assert response.status_code == 200
    assert "username" in response.json()
