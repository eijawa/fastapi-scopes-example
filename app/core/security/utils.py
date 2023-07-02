from fastapi import Depends
from fastapi.security import SecurityScopes

from app.core.http.exceptions import HTTP_401_UnauthorizedError

from .scheme import security_scheme
from .security import TokenData, decode_token


def verify_permissions(
    security_scopes: SecurityScopes, token: str = Depends(security_scheme)
):
    """
    Верификация прав доступа.

    Проверка того, что требуемые права доступа есть у данного пользователя в токене
    """

    token_data: TokenData | None = decode_token(token)
    if token_data is None:
        # Переданы неправильные данные в токене!
        raise HTTP_401_UnauthorizedError()
    
    for scope in security_scopes.scopes:
        # Здесь security_scopes.scopes
        # Является не list[str], как обычно,
        # а list[Permissions]
        if str(scope) not in token_data.scopes: # type: ignore
            raise HTTP_401_UnauthorizedError("Недостаточно прав!")
