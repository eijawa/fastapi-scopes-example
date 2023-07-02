from app.core.db.session import Session
from app.core.settings import settings
from app.crud.exp.sync import sync_permissions
from app.crud.repositories import PermissionsRepository, UsersRepository
from app.crud.services import UsersService
from app.schemas.user import CreateUserSchema


def pre_init():
    with Session() as session:
        if not PermissionsRepository.check_db_sync(session):
            if settings.DB_PERMISSIONS_SYNC_REQUIRED:
                # Установлен флаг на
                # синхронизацию данных о правах между кодом и базой данных
                sync_permissions(session)
            else:
                raise Exception("Permissions в коде не совпадают с Permissions базе!")

        if (
            UsersRepository.get_by_username(
                session, username=settings.DEFAULT_ADMIN_USERNAME
            )
            is None
        ):
            # В базе нет пользователя с админ-правами

            admin_user_schema = CreateUserSchema(
                username=settings.DEFAULT_ADMIN_USERNAME,
                password=settings.DEFAULT_ADMIN_PASSWORD,
            )

            UsersService.create_superuser(session, obj=admin_user_schema)
