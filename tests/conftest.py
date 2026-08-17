import os
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.dependencies.database import get_db
from app.enums.fm_import import ImportType, ImportUploadStatus
from app.main import app
from app.models.base import Base
from app.models.fm_import import Import
from app.models.save import Save
from tests.protocols import ImportFactory, SaveFactory

test_db_url = os.environ.get("TEST_POSTGRES_URL")


@pytest.fixture(scope="session")
def test_db() -> Generator[Engine, None, None]:
    test_engine = create_engine(test_db_url, echo=False)
    Base.metadata.create_all(test_engine)

    yield test_engine

    Base.metadata.drop_all(test_engine)
    test_engine.dispose()


@pytest.fixture(scope="session")
def testing_session_local(test_db: Engine) -> sessionmaker[Session]:
    return sessionmaker(
        bind=test_db,
        autoflush=False,
        autocommit=False,
    )


@pytest.fixture
def db_session(testing_session_local: sessionmaker[Session]) -> Generator[Session, None, None]:
    with testing_session_local() as session:
        yield session

        session.rollback()

        for table in reversed(Base.metadata.sorted_tables):
            session.execute(table.delete())

        session.commit()


@pytest.fixture
def override_db(testing_session_local: sessionmaker[Session]) -> Generator[None, None, None]:
    def override_get_db() -> Generator[Session, None, None]:
        with testing_session_local() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    yield

    app.dependency_overrides.clear()


@pytest.fixture
def client(
    test_db: Engine,
    override_db: None,
) -> TestClient:
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
        upload_status: ImportUploadStatus = ImportUploadStatus.STARTED,
        import_type: ImportType = ImportType.SQUAD,
        filename: str = "path/to/file",
        save_id: int | None = None,
    ) -> Import:
        if save_id is None:
            raise ValueError("Save id can not be None")

        import_ = Import(
            version=version,
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
