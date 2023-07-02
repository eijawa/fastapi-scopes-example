from typing import Any, Union
from pydantic import BaseModel
from sqlalchemy import exc as SQLAlchemyExceptions
from sqlalchemy.orm import Session

from app.core.security.permissions import Permissions, PermissionsGroups
from app.crud.repositories import PermissionsRepository, UsersPermissionsRepository
from app.models import PermissionModel, UserPermissionModel
from app.models.user import UserModel
from app.schemas.permission import (
    CreatePermissionSchema,
    CreateUserPermissionSchema,
    UpdatePermissionSchema,
)

from .service import BaseService


class PermissionsService(
    BaseService[PermissionModel, CreatePermissionSchema, UpdatePermissionSchema]
):
    model = PermissionModel


class UsersPermissionsService(
    BaseService[UserPermissionModel, CreateUserPermissionSchema, BaseModel]
):
    model = UserPermissionModel

    @classmethod
    def update(
        cls,
        session: Session,
        *,
        obj: UserPermissionModel,
        upd_obj: BaseModel | dict[str, Any],
    ):
        raise NotImplementedError()

    @classmethod
    def link(
        cls,
        session: Session,
        *,
        user: UserModel,
        permissions: list[str | Permissions | PermissionModel] = [],
        permissions_groups: list[PermissionsGroups] = [],
    ) -> None:
        """
        Метод выдачи прав пользователю на уровне базы данных
        """

        if not permissions and not permissions_groups:
            raise ValueError()

        perms_keys: set[str] = set()

        if permissions:
            if isinstance(permissions[0], Permissions):
                perms_keys.update([p.value.key for p in permissions])  # type: ignore
            elif isinstance(permissions[0], PermissionModel):
                perms_keys.update([p.name for p in permissions])  # type: ignore
            else:
                perms_keys.update(permissions)  # type: ignore

        for group in permissions_groups:
            perms_keys.update([p.value.key for p in group.value])

        perms_in_db = PermissionsRepository.get_all_by_names(
            session, names=perms_keys
        )

        for perm_in_db in perms_in_db:
            new_link = CreateUserPermissionSchema(
                user_id=user.id, permission_id=perm_in_db.id
            )

            cls.create(session, obj=new_link)

        # УСТАРЕЛО!!!
        #
        # По поводу использования UsersPermissionsRepository.has
        # см. docs\SDF\Проверка на обладание правами при связке пользователя с правами.md
        # if perm_in_db is not None and not UsersPermissionsRepository.has(
        #     session, user=user, permissions=[perm_in_db.name]
        # ):

        # for perm in perms:
        #     perm_in_db: PermissionModel | None = PermissionsRepository.get_by_name(
        #         session, name=perm.value.key
        #     )

        #     if perm_in_db is not None:
        #         new_link = CreateUserPermissionSchema(
        #             user_id=user.id, permission_id=perm_in_db.id
        #         )

        #         cls.create(session, obj=new_link)
