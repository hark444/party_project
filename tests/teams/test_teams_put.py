from fastapi import status
import json

DEFAULT_TEAMS_PAYLOAD = {"team_name": "mPulse"}

PUT_TEAMS_PAYLOAD = {"team_name": "mPulse-admin"}

teams_url = "/api/v1/teams"


def create_teams(client):
    response = client.post(teams_url, json=DEFAULT_TEAMS_PAYLOAD)
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()


def test_put_teams(client):
    teams_obj = create_teams(client)
    team_id = teams_obj.get("id")
    response = client.put(teams_url + f"/{team_id}", json=PUT_TEAMS_PAYLOAD)
    assert response.status_code == status.HTTP_200_OK

    response_json = response.json()
    assert response_json.get("team_name") == PUT_TEAMS_PAYLOAD["team_name"].lower()


# Since auth layer is open for teams, this test should pass
def test_put_teams_without_auth(client):
    teams_obj = create_teams(client)
    team_id = teams_obj.get("id")
    response = client.put(teams_url + f"/{team_id}", json=PUT_TEAMS_PAYLOAD)
    assert response.status_code == status.HTTP_200_OK


def test_put_team_with_incorrect_id(client):
    teams_obj = create_teams(client)
    team_id = teams_obj.get("id")
    response = client.put(teams_url + f"/{team_id+1}", json=PUT_TEAMS_PAYLOAD)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_put_team_with_existing_name(client):
    teams_obj = create_teams(client)
    team_id = teams_obj.get("id")
    response = client.put(teams_url + f"/{team_id+1}", json=DEFAULT_TEAMS_PAYLOAD)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    response_json = response.json()
    assert (
        response_json.get("detail")[0]["msg"]
        == "A team with the same name already exists. "
        "Please try to create a team with a different name. "
    )
