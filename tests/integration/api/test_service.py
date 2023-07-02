from fastapi import status

from tests.integration.client import client


def test_healthcheck():
    r = client.get("/api/v1/healthcheck")

    assert r.status_code == status.HTTP_200_OK
