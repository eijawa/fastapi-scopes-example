from app.api.deps import db_session
from app.main import app as HAFastAPI_app

from .overrides import override_db_session

HAFastAPI_app.dependency_overrides[db_session] = override_db_session
