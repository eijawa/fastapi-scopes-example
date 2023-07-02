from tests.db import TestingSessionLocal


def override_db_session():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
