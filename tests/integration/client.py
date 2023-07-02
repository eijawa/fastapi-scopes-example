from fastapi.testclient import TestClient

from .ext.app import HAFastAPI_app


client = TestClient(HAFastAPI_app)
