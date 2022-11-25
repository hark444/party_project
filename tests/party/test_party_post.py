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


def test_post_party(client, account_user_and_token):
    headers = {"Authorization": f'Bearer {account_user_and_token.get("access_token")}'}
    response = client.post(party_url, headers=headers, json=DEFAULT_PARTY_PAYLOAD)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("reason") == DEFAULT_PARTY_PAYLOAD.get("reason")
    assert response_json.get("guests_invited") == DEFAULT_PARTY_PAYLOAD.get(
        "guests_invited"
    )


def test_post_party_with_missing_proposed_date(client, account_user_and_token):
    headers = {"Authorization": f'Bearer {account_user_and_token.get("access_token")}'}
    del DEFAULT_PARTY_PAYLOAD["proposed_date"]
    response = client.post(party_url, headers=headers, json=DEFAULT_PARTY_PAYLOAD)
    assert response.status_code == 422


def test_post_party_without_auth(client, account_user_and_token):
    response = client.post(party_url, json=DEFAULT_PARTY_PAYLOAD)
    assert response.status_code == 401


def test_post_party_return_default_approved_and_ratings(client, account_user_and_token):
    headers = {"Authorization": f'Bearer {account_user_and_token.get("access_token")}'}
    response = client.post(party_url, headers=headers, json=DEFAULT_PARTY_PAYLOAD)
    assert response.status_code == 200
    response_json = response.json()
    assert not response_json.get("ratings")
    assert not response_json.get("approved")
