from sqlalchemy.orm import Session

from app.crud.services import UsersService
from app.schemas.user import CreateUserSchema


def register(session: Session, *, credentials: CreateUserSchema):
    """
    Зачем этот метод?
    Это обёртка на случай, если изменится способ регистрации
    """

    UsersService.create(session, obj=credentials)
