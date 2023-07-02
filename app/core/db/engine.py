from sqlalchemy import create_engine

from app.core.settings import settings


engine = create_engine(settings.DB_CONN_STRING, echo=True)
