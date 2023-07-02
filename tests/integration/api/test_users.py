from fastapi import status

from app.core.security.permissions import Permissions
from tests.integration.client import client
from tests.integration.ext.data import TEST_USER_CREDENTIALS, ADMIN_USER_CREDENTIALS
from tests.integration.utils import auth


@auth(**TEST_USER_CREDENTIALS, scopes=[Permissions.users_me])
def test_get_users_me_wcp():
    """
    Тестирование получения информации о пользователе с корретными правами
    """

    r = client.get("/api/v1/users/me")

    assert r.status_code == status.HTTP_200_OK, r.text

    data = r.json()

    assert "id" in data


@auth(**TEST_USER_CREDENTIALS, scopes=[])
def test_get_users_me_wip():
    """
    Тестирование получения информации о пользователе с некорретным набором прав
    """

    r = client.get("/api/v1/users/me")

    assert r.status_code == status.HTTP_401_UNAUTHORIZED, r.text


@auth(**ADMIN_USER_CREDENTIALS, scopes=[Permissions.users_read])
def test_get_all_users_wcp():
    """
    Тестирование получения информации обо всех пользователях с корректным набором прав
    """

    r = client.get("/api/v1/users")

    assert r.status_code == status.HTTP_200_OK, r.text

    data = r.json()
    assert data

    assert "id" in data[0], data


@auth(**ADMIN_USER_CREDENTIALS, scopes=[])
def test_get_all_users_wip():
    """
    Тестирование получения информации обо всех пользователях с некорректным набором прав
    """

    r = client.get("/api/v1/users")

    assert r.status_code == status.HTTP_401_UNAUTHORIZED, r.text
