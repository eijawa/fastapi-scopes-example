from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.models import UserModel
from app.crud.repositories import UsersRepository
from app.crud.services import UsersService
from app.core.security import password_manager

from .retriesmanager import retries_manager
from .exceptions import BadCredentialsError, MaxRetriesReachedError, UserBlockedError


def authenticate(
    session: Session, *, credentials: OAuth2PasswordRequestForm
) -> UserModel:
    user = UsersRepository.get_by_username(session, username=credentials.username)

    if user is None:
        raise BadCredentialsError()

    if not password_manager.verify(user.password, credentials.password):
        try:
            retries_manager.increase(user.id)

            raise BadCredentialsError()
        except MaxRetriesReachedError:
            UsersService.deactivate(session, obj=user)

            # Очищаем дополнительно память о входах пользователя
            retries_manager.purify(user.id)

            raise UserBlockedError()

    retries_manager.purify(user.id)

    if password_manager.check_needs_rehash(user.password):
        UsersService.rehash_password(session, obj=user, password=credentials.password)

    return user
