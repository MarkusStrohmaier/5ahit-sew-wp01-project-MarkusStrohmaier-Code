from fastapi.testclient import TestClient
from datetime import datetime
import pytest
import uuid

USER_BASE_URL = "/api/users"

def test_register_user(client_with_superuser: TestClient):
    unique_id = uuid.uuid4().hex[:6]
    
    REGISTER_URL = f"{USER_BASE_URL}/users/register" 

    user_data = {
        "username": f"TestUser_{unique_id}",
        "email": f"user_{unique_id}@test.com",
        "password": "Kennwort1"
    }

    response = client_with_superuser.post(REGISTER_URL, json=user_data)
    
    assert response.status_code == 200
    assert "username" in response.json()
    assert response.json()["username"] == user_data["username"]