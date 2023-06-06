from models.user import UserModel
from fastapi import status
import json
import pytest

DEFAULT_USER_PAYLOAD = {
    "email": "hkeshwani68@gmail.com",
    "password": "Test@123",
    "first_name": "Harshad",
    "last_name": "Keshwani",
}

DEFAULT_TEAMS_PAYLOAD = {"team_name": "mPulse"}

teams_url = "/api/v1/teams"


def create_teams(client):
    response = client.post(teams_url, json=DEFAULT_TEAMS_PAYLOAD)
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()


@pytest.mark.skip(reason="Not updating team in user api")
def test_create_user_with_invalid_team(client):
    DEFAULT_USER_PAYLOAD["team_name"] = "No Team"
    response = client.post(f"/api/v1/users", json=DEFAULT_USER_PAYLOAD)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    response_data = json.loads(response.text)
    assert (
        response_data.get("detail")[0]["msg"]
        == "There is no existing team with this name."
    )


def test_create_user(client):
    response = client.post(f"/api/v1/users", json=DEFAULT_USER_PAYLOAD)
    assert response.status_code == status.HTTP_201_CREATED
    response_data = json.loads(response.text)
    assert response_data.get("email") == DEFAULT_USER_PAYLOAD.get("email")
    assert not response_data.get("disabled")


def test_create_user_with_missing_email(client):
    del DEFAULT_USER_PAYLOAD["email"]
    response = client.post(f"/api/v1/users", json=DEFAULT_USER_PAYLOAD)
    response_data = json.loads(response.text)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response_data.get("detail")[0]["msg"] == "field required"
