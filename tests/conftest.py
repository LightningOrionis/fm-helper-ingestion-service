import datetime
import os
import tempfile
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.database import postgresql
from app.enums.fm_import import ImportType, ImportUploadStatus
from app.main import app
from app.models.base import Base
from app.models.fm_import import Import
from app.models.save import Save
from tests.protocols import ImportFactory, SaveFactory

test_db_url = os.environ.get("TEST_POSTGRES_URL")
if not test_db_url:
    temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
    test_db_url = f"sqlite:///{temp_db.name}"

os.environ["POSTGRES_URL"] = test_db_url

test_engine = None


@pytest.fixture(scope="function")
def test_db() -> Generator[Engine, None, None]:
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
def db_session(test_db: Engine) -> Generator[Session, None, None]:
    SessionLocal = sessionmaker(
        bind=test_db,
        autoflush=False,
        autocommit=False,
    )

    with SessionLocal() as session:
        yield session


@pytest.fixture
def client(test_db: Engine) -> TestClient:
    return TestClient(app)


@pytest.fixture
def save_factory(db_session: Session) -> SaveFactory:
    def create_save(name: str = "save") -> Save:
        save = Save(name=name)
        db_session.add(save)
        db_session.commit()
        db_session.refresh(save)
        return save

    return create_save


@pytest.fixture
def import_factory(db_session: Session) -> ImportFactory:
    def create_import(
        version: int = 0,
        upload_date: datetime.datetime | None = None,
        upload_status: ImportUploadStatus = ImportUploadStatus.STARTED,
        import_type: ImportType = ImportType.SQUAD,
        filename: str = "path/to/file",
        save_id: int | None = None,
    ) -> Import:
        if save_id is None:
            raise ValueError("Save id can not be None")

        import_ = Import(
            version=version,
            upload_date=datetime.datetime.now() if not upload_date else upload_date,
            upload_status=upload_status,
            import_type=import_type,
            filename=filename,
            save_id=save_id,
        )
        db_session.add(import_)
        db_session.commit()
        db_session.refresh(import_)
        return import_

    return create_import
