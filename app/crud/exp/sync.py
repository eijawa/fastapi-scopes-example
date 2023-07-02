from sqlalchemy.orm import Session

from app.core.security.permissions import Permissions
from app.crud.repositories import PermissionsRepository
from app.crud.services import PermissionsService
from app.models.permission import PermissionModel
from app.schemas.permission import CreatePermissionSchema, UpdatePermissionSchema


def sync_permissions(session: Session) -> None:
    """
    Синхронизация прав из кода с базой данных
    """

    # Здесь нельзя применить массовое получение одним запросом,
    # поскольку нам нужно либо создать право, либо обновить его

    for perm in Permissions:
        perm_in_db: PermissionModel | None = PermissionsRepository.get_by_name(
            session, name=perm.value.key
        )

        if perm_in_db is None:
            # Create
            new_perm = CreatePermissionSchema(
                name=perm.value.key, description=perm.value.description
            )
            PermissionsService.create(session, obj=new_perm)
        else:
            # Update
            upd_perm = UpdatePermissionSchema(description=perm.value.description)
            PermissionsService.update(session, obj=perm_in_db, upd_obj=upd_perm)
