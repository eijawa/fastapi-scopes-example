from fastapi import Depends
from sqlalchemy.orm import Session as SQLAlchemySession

from app.core.db import Session
from app.core.http.exceptions import HTTP_401_UnauthorizedError, HTTP_403_ForbiddenError
from app.core.security import TokenData, decode_token
from app.core.security.scheme import security_scheme
from app.crud.repositories import UsersRepository
from app.crud.services import UsersService
from app.models import UserModel


def db_session():
    s = Session()
    try:
        yield s
    finally:
        s.close()


def get_current_user(
    session: SQLAlchemySession = Depends(db_session),
    token: str = Depends(security_scheme),
) -> UserModel:
    token_data: TokenData | None = decode_token(token)
    if token_data is None:
        # Переданы неправильные данные в токене!
        raise HTTP_401_UnauthorizedError()
    
    user: UserModel | None = UsersRepository.get(session, pk=token_data.id)

    if user is None:
        # Значит, произошла какая-то фигня 
        # и у нас здесь токен от несуществующего или удалённого пользователя
        raise HTTP_401_UnauthorizedError()

    UsersService.update_last_access(session, obj=user)

    return user


def get_current_active_user(user: UserModel = Depends(get_current_user)):
    if not user.is_active:
        # Пользователь заблокирован!
        raise HTTP_403_ForbiddenError()
    
    return user
