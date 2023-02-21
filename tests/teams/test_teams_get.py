from fastapi import status
import json

DEFAULT_TEAMS_PAYLOAD = {"team_name": "mPulse"}

teams_url = "/api/v1/teams"


def create_teams(client):
    response = client.post(teams_url, json=DEFAULT_TEAMS_PAYLOAD)
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()


def test_get_all_teams(client):
    teams_obj = create_teams(client)
    response = client.get(teams_url)
    assert response.status_code == status.HTTP_200_OK

    response_json = response.json()
    assert response_json.get("total") == 1
    assert (
        response_json.get("data")[0].get("team_name")
        == DEFAULT_TEAMS_PAYLOAD["team_name"].lower()
    )


# Since auth layer is open for teams, this test should pass
def test_get_teams_without_auth(client):
    teams_obj = create_teams(client)
    response = client.get(teams_url)
    assert response.status_code == status.HTTP_200_OK


def test_get__team_by_id(client):
    teams_obj = create_teams(client)
    team_id = teams_obj.get("id")
    response = client.get(teams_url + f"/{team_id}")

    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    assert response_json.get("team_name") == DEFAULT_TEAMS_PAYLOAD["team_name"].lower()


def test_get_team_with_incorrect_id(client):
    teams_obj = create_teams(client)
    team_id = teams_obj.get("id")
    response = client.get(teams_url + f"/{team_id+1}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
