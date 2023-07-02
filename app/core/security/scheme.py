from fastapi.security import OAuth2PasswordBearer

from app.core.security.permissions import Permissions
from app.core.settings import settings

security_scheme = OAuth2PasswordBearer(
    tokenUrl=settings.DEFAULT_AUTH_URL, scopes=Permissions.dict()
)
