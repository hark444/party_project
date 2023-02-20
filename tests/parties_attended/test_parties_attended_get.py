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

DEFAULT_PARTIES_ATTENDED_PAYLOAD = {
    "rating": 5,
    "approved": True,
    "comment": "Awesome party bro!",
}
party_url = "/api/v1/party"
parties_attended_url = "/api/v1/parties_attended"


def create_party_object(client, headers):
    create_party = client.post(party_url, headers=headers, json=DEFAULT_PARTY_PAYLOAD)
    assert create_party.status_code == 200
    return create_party.json()


def create_party_attended_object(client, headers, party_obj):
    DEFAULT_PARTIES_ATTENDED_PAYLOAD["party_id"] = party_obj.get("id")
    party_attended_obj = client.post(
        parties_attended_url, headers=headers, json=DEFAULT_PARTIES_ATTENDED_PAYLOAD
    )
    assert party_attended_obj.status_code == 200
    return party_attended_obj


def test_get_all_parties_attended(client, account_user_and_token):
    headers = {"Authorization": f'Bearer {account_user_and_token.get("access_token")}'}
    party_obj = create_party_object(client, headers)
    party_attended_obj = create_party_attended_object(client, headers, party_obj)
    response = client.get(parties_attended_url, headers=headers)
    response_json = response.json()
    assert response_json.get("total") == 1
    assert response_json.get("data")[0].get("party_id") == party_obj.get("id")


def test_get_single_party_attended(client, account_user_and_token):
    headers = {"Authorization": f'Bearer {account_user_and_token.get("access_token")}'}
    party_obj = create_party_object(client, headers)
    party_attended_obj = create_party_attended_object(client, headers, party_obj)
    get_party_attended_url = (
        parties_attended_url + f"/{party_attended_obj.json().get('id')}"
    )
    response = client.get(get_party_attended_url, headers=headers)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("comment") == DEFAULT_PARTIES_ATTENDED_PAYLOAD.get(
        "comment"
    )


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


def test_get_parties_attended_for_empty_party(client, account_user_and_token):
    headers = {"Authorization": f'Bearer {account_user_and_token.get("access_token")}'}
    response = client.get(parties_attended_url, headers=headers)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("total") == 0
