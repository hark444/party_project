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


def test_delete_party(client, account_user_and_token):
    headers = {"Authorization": f'Bearer {account_user_and_token.get("access_token")}'}
    party_obj = create_party_object(client, headers)
    party_put_url = party_url + f'/{party_obj.get("id")}'
    response = client.delete(party_put_url, headers=headers)
    assert response.status_code == 200


def test_delete_party_with_missing_auth(client, account_user_and_token):
    headers = {"Authorization": f'Bearer {account_user_and_token.get("access_token")}'}
    party_obj = create_party_object(client, headers)
    party_put_url = party_url + f'/{party_obj.get("id")}'
    response = client.delete(party_put_url)
    assert response.status_code == 401
