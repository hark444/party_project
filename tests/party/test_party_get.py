from models.user import UserModel
from fastapi import status
import json
from tests.conftest import DEFAULT_USER_PAYLOAD
from datetime import datetime

DEFAULT_PARTY_PAYLOAD = {
    "reason": "Test Party",
    "proposed_date": str(datetime.now()),
    "guests_invited": 5,
    "party_date": str(datetime.now()),
    "party_place": "Nagar Nigam",
}
party_url = "/api/v1/party"


def create_party_object(client, headers):
    create_party = client.post(party_url, headers=headers, json=DEFAULT_PARTY_PAYLOAD)
    assert create_party.status_code == 200
    return create_party.json()


def test_get_all_party(client, account_user_and_token):
    headers = {"Authorization": f'Bearer {account_user_and_token.get("access_token")}'}
    party_obj = create_party_object(client, headers)
    response = client.get(party_url, headers=headers)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("total") == 1
    assert response_json.get("data")[0].get("reason") == DEFAULT_PARTY_PAYLOAD.get(
        "reason"
    )


def test_get_single_party(client, account_user_and_token):
    headers = {"Authorization": f'Bearer {account_user_and_token.get("access_token")}'}
    party_obj = create_party_object(client, headers)
    party_get_url = party_url + f"/{party_obj.get('id')}"
    response = client.get(party_get_url, headers=headers)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("reason") == DEFAULT_PARTY_PAYLOAD.get("reason")


def test_get_single_party_with_incorrect_party_id(client, account_user_and_token):
    headers = {"Authorization": f'Bearer {account_user_and_token.get("access_token")}'}
    party_obj = create_party_object(client, headers)
    party_get_url = party_url + f"/{party_obj.get('id') + 1}"
    response = client.get(party_get_url, headers=headers)
    assert response.status_code == 404
    response_json = response.json()
    assert (
        response_json.get("detail") == "No Party object for this party id and user id"
    )


def test_get_party_for_empty_party(client, account_user_and_token):
    headers = {"Authorization": f'Bearer {account_user_and_token.get("access_token")}'}
    response = client.get(party_url, headers=headers)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("total") == 0
