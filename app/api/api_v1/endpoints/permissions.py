from typing import Any

from fastapi import APIRouter, Depends, Security, Response, status
from sqlalchemy.orm import Session

from app.api.deps import db_session, get_current_active_user
from app.core.http.exceptions import HTTP_404_NotFoundError
from app.core.security.permissions import Permissions
from app.core.security.utils import verify_permissions
from app.core.utils.text import required_permissions_str
from app.crud.repositories import (
    PermissionsRepository,
    UsersPermissionsRepository,
    UsersRepository,
)
from app.models import PermissionModel, UserModel
from app.schemas.permission import (
    ComputedPermissionSchema,
    PermissionSchema,
    UserPermissions,
)
from app.crud.services import UsersPermissionsService

router = APIRouter()


@router.get(
    "/permissions",
    description=required_permissions_str(Permissions.permissions_read),
    response_model=list[ComputedPermissionSchema],
    dependencies=[
        Security(verify_permissions, scopes=[str(Permissions.permissions_read)])
    ],
)
async def get_all_permissions(
    session: Session = Depends(db_session),
) -> list[Any]:
    """
    Получение списка Permissions с флагом о присутствии в коде
    """

    perms: list[PermissionModel] = PermissionsRepository.all(session)
    prems_in_code_keys: list[str] = [
        p.value.key for p in Permissions.__members__.values()
    ]

    for perm_in_db in perms:
        if perm_in_db.name in prems_in_code_keys:
            setattr(perm_in_db, "is_in_code", True)

    return perms


@router.get(
    "/users/me/permissions",
    tags=["users"],
    response_model=UserPermissions,
    description=required_permissions_str(Permissions.permissions_me),
    dependencies=[
        Security(verify_permissions, scopes=[str(Permissions.permissions_me)])
    ],
)
async def get_current_user_permissions(
    session: Session = Depends(db_session),
    user: UserModel = Depends(get_current_active_user),
) -> UserPermissions:
    return get_user_permissions_pretty(session, user=user)


@router.get(
    "/users/me/{user_id}/permissions",
    tags=["users"],
    response_model=UserPermissions,
    description=required_permissions_str(Permissions.permissions_read),
    dependencies=[
        Security(verify_permissions, scopes=[str(Permissions.permissions_read)])
    ],
)
async def get_user_permissions(
    user_id: int, session: Session = Depends(db_session)
) -> UserPermissions:
    user: UserModel | None = UsersRepository.get(session, pk=user_id)

    if user is None:
        raise HTTP_404_NotFoundError(f"Пользователя с {user_id=} не существует!")

    return get_user_permissions_pretty(session, user=user)


@router.post(
    "/users/me/{user_id}/permissions",
    tags=["users"],
    description=required_permissions_str(Permissions.permissions_create),
    dependencies=[
        Security(verify_permissions, scopes=[str(Permissions.permissions_create)])
    ],
)
async def add_permissions_to_user(
    user_id: int, permissions_keys: list[str], session: Session = Depends(db_session)
) -> Response:
    user: UserModel | None = UsersRepository.get(session, pk=user_id)

    if user is None:
        raise HTTP_404_NotFoundError(f"Пользователя с {user_id=} не существует!")

    UsersPermissionsService.link(session, user=user, permissions=permissions_keys)  # type: ignore

    return Response(status_code=status.HTTP_200_OK)


@router.delete(
    "/users/me/{user_id}/permissions/{permission_id}",
    tags=["users"],
    description=required_permissions_str(Permissions.permissions_delete),
    dependencies=[
        Security(verify_permissions, scopes=[str(Permissions.permissions_delete)])
    ],
)
async def delete_permission_from_user(
    user_id: int, permission_id: int, session: Session = Depends(db_session)
) -> Response:
    UsersPermissionsService.delete(
        session, pk={"user_id": user_id, "permission_id": permission_id}
    )

    return Response(status_code=status.HTTP_200_OK)


def get_user_permissions_pretty(
    session: Session, *, user: UserModel
) -> UserPermissions:
    u_perms_in_db = UsersPermissionsRepository.get_by_user(session, user=user)

    user_permissions = UserPermissions(id=user.id, username=user.username)
    for perm_in_db in u_perms_in_db:
        user_permissions.permissions.append(
            PermissionSchema.from_orm(perm_in_db.permission)
        )

    return user_permissions
