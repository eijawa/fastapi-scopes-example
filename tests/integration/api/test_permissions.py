from fastapi import status

from app.core.security.permissions import Permissions

from tests.integration.client import client
from tests.integration.utils import auth
from tests.integration.ext.data import ADMIN_USER_CREDENTIALS, TEST_USER_CREDENTIALS


@auth(**ADMIN_USER_CREDENTIALS, scopes=[Permissions.permissions_read])
def test_get_all_permissions_wcp():
    """
    Тестирование получения списка всех доступных прав
    """

    r = client.get("/api/v1/permissions")

    assert r.status_code == status.HTTP_200_OK, r.text

    data = r.json()

    assert data, data

    assert "id" in data[0]


@auth(**ADMIN_USER_CREDENTIALS, scopes=[])
def test_get_all_permissions_wip():
    """
    Тестирование получения списка всех доступных прав с некорретными правами
    """

    r = client.get("/api/v1/permissions")

    assert r.status_code == status.HTTP_401_UNAUTHORIZED, r.text
