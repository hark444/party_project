from fastapi import status
import json

DEFAULT_TEAMS_PAYLOAD = {"team_name": "mPulse"}

teams_url = "/api/v1/teams"


def test_post_teams(client):
    response = client.post(teams_url, json=DEFAULT_TEAMS_PAYLOAD)
    assert response.status_code == status.HTTP_201_CREATED
    response_json = response.json()
    assert (
        response_json.get("team_name") == DEFAULT_TEAMS_PAYLOAD.get("team_name").lower()
    )


# Since auth layer is open for teams, this test should pass
def test_post_teams_without_auth(client):
    response = client.post(teams_url, json=DEFAULT_TEAMS_PAYLOAD)
    assert response.status_code == status.HTTP_201_CREATED


def test_post_team_with_same_name(client, account_user_and_token):
    response = client.post(teams_url, json=DEFAULT_TEAMS_PAYLOAD)
    assert response.status_code == status.HTTP_201_CREATED
    response = client.post(teams_url, json=DEFAULT_TEAMS_PAYLOAD)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    response_json = response.json()
    assert (
        response_json.get("detail")[0]["msg"]
        == "A team with the same name already exists. "
        "Please try to create a team with a different name. "
    )
