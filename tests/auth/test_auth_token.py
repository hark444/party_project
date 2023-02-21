from models.user import UserModel
from fastapi import status
import json


DEFAULT_USER_PAYLOAD = {
    "email": "hkeshwani68@gmail.com",
    "password": "Test@123",
    "first_name": "Harshad",
    "last_name": "Keshwani",
}


def test_create_user_token(client):
    response = client.post(f"/api/v1/users", json=DEFAULT_USER_PAYLOAD)
    assert response.status_code == status.HTTP_201_CREATED
    response = client.post(f"/api/v1/auth/token", json=DEFAULT_USER_PAYLOAD)
    assert response.status_code == status.HTTP_201_CREATED
    response_data = json.loads(response.text)
    assert response_data.get("access_token")
    assert response_data.get("token_type") == "bearer"


# TODO: Write negative cases as well.
