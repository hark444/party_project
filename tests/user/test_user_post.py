from models.user import UserModel
from fastapi import status
import json


def test_create_user(client):
    payload = {
        "email": "hkeshwani68@gmail.com",
        "password": "Test@123",
        "first_name": "Harshad",
        "last_name": "Keshwani",
    }
    response = client.post(f"/api/v1/users/create", data=payload)
    assert response.status_code == status.HTTP_200_OK
    response_data = json.loads(response.text)
    assert response_data.get("email") == payload.get("email")
    assert not response_data.get("disabled")


def test_create_user_with_missing_email(client):
    payload = {
        "email": "hkeshwani68@gmail.com",
        "password": "Test@123",
        "first_name": "Harshad",
        "last_name": "Keshwani",
    }
    del payload["email"]
    response = client.post(f"/api/v1/users/create", data=payload)
    response_data = json.loads(response.text)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response_data == {
        "detail": [
            {
                "loc": ["body", "email"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }
