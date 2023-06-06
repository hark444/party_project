from models.user import UserModel
from fastapi import status
import json

DEFAULT_USER_PAYLOAD = {
    "first_name": "Harshad",
    "last_name": "Keshwani",
}

"""
# This case needs to be handled differently.
def test_update_user(client, account_user_and_token):
    headers = {"Authorization": f'Bearer {account_user_and_token.get("access_token")}'}
    DEFAULT_USER_PAYLOAD["team"] = "MPulse"
    response = client.put("/api/v1/users", headers=headers, json=DEFAULT_USER_PAYLOAD)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("team") == "MPulse"
"""


def test_update_user_email_should_not_work(client, account_user_and_token):
    headers = {"Authorization": f'Bearer {account_user_and_token.get("access_token")}'}
    DEFAULT_USER_PAYLOAD["email"] = "hkeshwani68@gmail.com"
    response = client.put("/api/v1/users", headers=headers, json=DEFAULT_USER_PAYLOAD)
    assert response.status_code == 200
    response_json = response.json()
    assert not response_json.get("email") == "hkeshwani68@gmail.com"
