from app.core.security.permissions import Permissions

from tests.integration.client import client


def contruct_auth_header(access_token: str, token_type: str) -> dict[str, str]:
    return {"Authorization": f"{token_type.title()} {access_token}"}


def auth(username: str, password: str, scopes: list[Permissions]):
    def decorator(func):
        def wrapper(*args, **kwargs):
            r = client.post("/api/v1/auth/login", data={
                "username": username,
                "password": password,
                "grant_type": "password",
                "scope": " ".join([p.value.key for p in scopes])
            })

            client.headers.update(contruct_auth_header(**r.json()))

            result = func(*args, **kwargs)

            del client.headers["Authorization"]

            return result
        
        return wrapper
    
    return decorator
