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

DEFAULT_PARTY_PUT_PAYLOAD = {
    "reason": "Test Party",
    "proposed_date": str(datetime.now()),
    "guests_invited": 5,
    "party_date": str(datetime.now()),
    "party_place": "Nagar Nigam Updated",
}
party_url = "/api/v1/party"


def create_party_object(client, headers):
    create_party = client.post(party_url, headers=headers, json=DEFAULT_PARTY_PAYLOAD)
    assert create_party.status_code == 200
    return create_party.json()


def test_put_party(client, account_user_and_token):
    headers = {"Authorization": f'Bearer {account_user_and_token.get("access_token")}'}
    party_obj = create_party_object(client, headers)
    party_put_url = party_url + f'/{party_obj.get("id")}'
    response = client.put(party_put_url, headers=headers, json=DEFAULT_PARTY_PUT_PAYLOAD)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("party_place") == DEFAULT_PARTY_PUT_PAYLOAD.get("party_place")


def test_put_party_with_missing_auth(client, account_user_and_token):
    headers = {"Authorization": f'Bearer {account_user_and_token.get("access_token")}'}
    party_obj = create_party_object(client, headers)
    party_put_url = party_url + f'/{party_obj.get("id")}'
    response = client.put(party_put_url, json=DEFAULT_PARTY_PUT_PAYLOAD)
    assert response.status_code == 401


def test_put_party_update_approved_and_ratings(client, account_user_and_token):
    headers = {"Authorization": f'Bearer {account_user_and_token.get("access_token")}'}
    party_obj = create_party_object(client, headers)
    party_put_url = party_url + f'/{party_obj.get("id")}'
    DEFAULT_PARTY_PUT_PAYLOAD["ratings"] = 5.1
    DEFAULT_PARTY_PUT_PAYLOAD["approved"] = True
    response = client.put(party_put_url, headers=headers, json=DEFAULT_PARTY_PUT_PAYLOAD)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("ratings") == DEFAULT_PARTY_PUT_PAYLOAD.get("ratings")
    assert response_json.get("approved") == DEFAULT_PARTY_PUT_PAYLOAD.get("approved")


def test_put_party_with_missing_proposed_date(client, account_user_and_token):
    headers = {"Authorization": f'Bearer {account_user_and_token.get("access_token")}'}
    party_obj = create_party_object(client, headers)
    party_put_url = party_url + f'/{party_obj.get("id")}'
    del DEFAULT_PARTY_PUT_PAYLOAD["proposed_date"]
    response = client.put(party_put_url, headers=headers, json=DEFAULT_PARTY_PUT_PAYLOAD)
    assert response.status_code == 422
