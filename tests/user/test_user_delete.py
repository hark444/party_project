from models.user import UserModel
from fastapi import status
import json

DEFAULT_USER_PAYLOAD = {
    "email": "hkeshwani68@gmail.com",
    "password": "Test@123",
    "first_name": "Harshad",
    "last_name": "Keshwani",
}


def test_delete_user(client, account_user_and_token):
    headers = {"Authorization": f'Bearer {account_user_and_token.get("access_token")}'}
    del_response = client.delete("/api/v1/users", headers=headers)
    assert del_response.status_code == 200
    response_json = del_response.json()
    assert not response_json


def test_delete_user_with_missing_auth(client):
    del_response = client.delete("/api/v1/users")
    assert del_response.status_code == 401
