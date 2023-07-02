from app.core.db.modelbase import ModelBase
from app.crud.exp.sync import sync_permissions
from app.crud.services import UsersService
from app.schemas.user import CreateUserSchema
from tests.integration.ext.data import ADMIN_USER_CREDENTIALS

from .db import TestingSessionLocal, engine


def pytest_sessionstart(session):
    ModelBase.metadata.create_all(bind=engine)

    with TestingSessionLocal() as session_:
        sync_permissions(session_)

        UsersService.create_superuser(
            session_, obj=CreateUserSchema(**ADMIN_USER_CREDENTIALS)
        )
