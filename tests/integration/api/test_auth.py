from fastapi import status

from tests.integration.client import client
from tests.integration.ext.data import TEST_USER_CREDENTIALS


def test_registration():
    """
    Тестирование регистрации пользователя
    """

    r = client.post(
        "/api/v1/auth/registration",
        json=TEST_USER_CREDENTIALS,
    )

    assert r.status_code == status.HTTP_201_CREATED


def test_registration_with_occupied_username():
    """
    Тестирование регистрации пользователя с уже занятым username
    """

    r = client.post("/api/v1/auth/registration", json=TEST_USER_CREDENTIALS)

    assert r.status_code == status.HTTP_409_CONFLICT


def test_login():
    """
    Тестирование авторизации пользователя
    """

    r = client.post(
        "/api/v1/auth/login",
        data={**TEST_USER_CREDENTIALS, "grant_type": "password", "scope": ""},
    )

    assert r.status_code == status.HTTP_200_OK, r.text


def test_login_with_unavailable_rights():
    """
    Тестирование авторизации пользователя с получением недоступных прав
    """

    r = client.post(
        "/api/v1/auth/login",
        data={**TEST_USER_CREDENTIALS, "grant_type": "password", "scope": "users:read"},
    )

    assert r.status_code == status.HTTP_401_UNAUTHORIZED, r.text


def test_login_with_incorrect_credentials():
    """
    Тестирование авторизации пользователя с некорректными данными для входа
    """

    incorrect_test_user_credentials = TEST_USER_CREDENTIALS.copy()
    incorrect_test_user_credentials["password"] = "somepasswordhere"

    r = client.post(
        "/api/v1/auth/login",
        data={**incorrect_test_user_credentials, "grant_type": "password", "scope": ""},
    )

    assert r.status_code == status.HTTP_400_BAD_REQUEST, r.text
