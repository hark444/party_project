from models.user import UserModel
from fastapi import status
import json
import pytest
from tests.conftest import DEFAULT_USER_PAYLOAD


DEFAULT_USER_PAYLOAD = {
    "email": "hkeshwani68@gmail.com",
    "password": "Test@123",
    "first_name": "Harshad",
    "last_name": "Keshwani",
    "date_of_joining": "2020-10-10",
}

DEFAULT_TEAMS_PAYLOAD = {"team_name": "mPulse"}

urls = {"users": "/api/v1/users", "teams": "/api/v1/teams"}


def create_teams(client):
    response = client.post(urls.get("teams"), json=DEFAULT_TEAMS_PAYLOAD)
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()


def create_user(client):
    team_obj = create_teams(client)
    DEFAULT_USER_PAYLOAD["team_name"] = team_obj.get("team_name")
    response = client.post(urls.get("users"), json=DEFAULT_USER_PAYLOAD)
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()


def test_users_get(client, account_user_and_token):
    create_user(client)
    response = client.get(urls.get("users"))
    assert response.status_code == 200
    response_data = response.json()
    assert response_data.get("total") == 2


@pytest.mark.skip()
def test_users_get_with_no_teams(client, account_user_and_token):
    create_user(client)
    params = {"team": False}
    response = client.get(urls.get("users"), params=params)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data.get("total") == 1
    assert response_data.get("data")[0]["id"] == account_user_and_token.get("user_id")


@pytest.mark.skip()
def test_users_get_with_teams(client, account_user_and_token):
    team_user = create_user(client)
    params = {"team": True, "team_name": DEFAULT_TEAMS_PAYLOAD["team_name"]}
    response = client.get(urls.get("users"), params=params)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data.get("total") == 1
    assert response_data.get("data")[0]["id"] == team_user.get("id")


@pytest.mark.skip()
def test_users_get_with_invalid_teams(client, account_user_and_token):
    create_user(client)
    params = {"team": True, "team_name": "invalid_team"}
    response = client.get(urls.get("users"), params=params)
    assert response.status_code == 422
    response_data = response.json()
    assert response_data.get("detail") == "There is no existing team with this name."


def test_users_get_with_team_name_and_disabled_team_flag(
    client, account_user_and_token
):
    create_user(client)
    params = {"team": False, "team_name": DEFAULT_TEAMS_PAYLOAD["team_name"]}
    response = client.get(urls.get("users"), params=params)
    assert response.status_code == 422
    response_data = response.json()
    assert (
        response_data.get("detail")
        == "The team flag is disabled but the team name is given."
    )


def test_users_get_with_experience(client, account_user_and_token):
    team_user = create_user(client)
    params = {"experience": 2}
    response = client.get(urls.get("users"), params=params)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data.get("total") == 1
    assert response_data.get("data")[0]["id"] == team_user.get("id")


def test_users_get_with_date_of_joining(client, account_user_and_token):
    team_user = create_user(client)
    params = {"doj": DEFAULT_USER_PAYLOAD["date_of_joining"]}
    response = client.get(urls.get("users"), params=params)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data.get("total") == 1
    assert response_data.get("data")[0]["id"] == team_user.get("id")
