from fastapi import APIRouter, Depends, Response, Security, status
from sqlalchemy.orm import Session

from app.api.deps import db_session, get_current_active_user
from app.core.http.exceptions import HTTP_404_NotFoundError
from app.core.security.permissions import Permissions
from app.core.security.utils import verify_permissions
from app.core.utils.text import required_permissions_str
from app.crud.repositories import UsersRepository
from app.crud.services import UsersService
from app.models import UserModel
from app.schemas.user import UserSchema

router = APIRouter()


@router.get(
    "/",
    description=required_permissions_str(Permissions.users_read),
    response_model=list[UserSchema],
    dependencies=[Security(verify_permissions, scopes=[str(Permissions.users_read)])],
)
async def get_all_users(session: Session = Depends(db_session)) -> list[UserModel]:
    return UsersRepository.all(session)


@router.get(
    "/me",
    description=required_permissions_str(Permissions.users_me),
    response_model=UserSchema,
    dependencies=[Security(verify_permissions, scopes=[str(Permissions.users_me)])],
)
async def get_user_self(
    user: UserModel = Depends(get_current_active_user),
) -> UserModel:
    return user


@router.post(
    "/me/{id}/activate",
    description=required_permissions_str(Permissions.users_update),
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Пользователь с заданным `id` не найден!"
        }
    },
    dependencies=[Security(verify_permissions, scopes=[str(Permissions.users_update)])],
    deprecated=True,  # См. docs\SDF\Отдельные методы activate и deactivate.md
)
async def activate_user(id: int, session: Session = Depends(db_session)) -> Response:
    user: UserModel | None = UsersRepository.get(session, pk=id)

    if user is None:
        raise HTTP_404_NotFoundError(f"Пользователь с заданным {id=} не найден!")

    UsersService.activate(session, obj=user)

    return Response(status_code=status.HTTP_200_OK)


@router.post(
    "/me/{id}/deactivate",
    description=required_permissions_str(Permissions.users_update),
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Пользователь с заданным `id` не найден!"
        }
    },
    dependencies=[Security(verify_permissions, scopes=[str(Permissions.users_update)])],
    deprecated=True,  # См. docs\SDF\Отдельные методы activate и deactivate.md
)
async def deactivate_user(id: int, session: Session = Depends(db_session)) -> Response:
    user: UserModel | None = UsersRepository.get(session, pk=id)

    if user is None:
        raise HTTP_404_NotFoundError(f"Пользователь с заданным {id=} не найден!")

    UsersService.deactivate(session, obj=user)

    return Response(status_code=status.HTTP_200_OK)
