from models.user import RoleTypeEnum
from fastapi import status


def test_default_user_role_is_regular(client, account_user_and_token):
    headers = {"Authorization": f'Bearer {account_user_and_token.get("access_token")}'}
    response = client.get("/api/v1/auth/define-me", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data.get("role") == RoleTypeEnum.regular


def test_superuser_can_update_role(client, superuser_and_token):
    headers = {"Authorization": f'Bearer {superuser_and_token.get("access_token")}'}
    user_id = superuser_and_token.get("user_id")
    payload = {"role": RoleTypeEnum.admin}
    response = client.patch(
        f"/api/v1/user-role/{user_id}", json=payload, headers=headers
    )
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data.get("role") == RoleTypeEnum.admin


def test_regular_cannot_update_role(client, account_user_and_token):
    headers = {"Authorization": f'Bearer {account_user_and_token.get("access_token")}'}
    user_id = account_user_and_token.get("user_id")
    response = client.patch(f"/api/v1/user-role/{user_id}", headers=headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json().get("detail") == "Not enough permissions."


def test_role_update_with_missing_data(client, superuser_and_token):
    headers = {"Authorization": f'Bearer {superuser_and_token.get("access_token")}'}
    user_id = superuser_and_token.get("user_id")
    response = client.patch(f"/api/v1/user-role/{user_id}", headers=headers)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    response_data = response.json()
    assert response_data == {
        "detail": [
            {"loc": ["body"], "msg": "field required", "type": "value_error.missing"}
        ]
    }


def test_admin_cannot_update_role(client, admin_user_and_token):
    headers = {"Authorization": f'Bearer {admin_user_and_token.get("access_token")}'}
    user_id = admin_user_and_token.get("user_id")
    response = client.patch(f"/api/v1/user-role/{user_id}", headers=headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json().get("detail") == "Not enough permissions."
