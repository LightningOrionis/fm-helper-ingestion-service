import os
import tempfile

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import postgresql
from app.main import app
from app.models.base import Base

test_db_url = os.environ.get("TEST_POSTGRES_URL")
if not test_db_url:
    temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
    test_db_url = f"sqlite:///{temp_db.name}"

os.environ["POSTGRES_URL"] = test_db_url

test_engine = None


@pytest.fixture(scope="function")
def test_db():
    global test_engine

    test_engine = create_engine(test_db_url, echo=False)
    Base.metadata.create_all(test_engine)

    def override_get_engine():
        return test_engine

    def override_get_session_maker():
        return sessionmaker(bind=test_engine, autoflush=False, autocommit=False)

    postgresql.get_engine = override_get_engine
    postgresql.get_session_maker = override_get_session_maker

    yield test_engine

    Base.metadata.drop_all(test_engine)
    test_engine.dispose()


@pytest.fixture
def client(test_db):
    return TestClient(app)
