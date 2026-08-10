from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import get_postgresql_settings


def get_engine():
    settings = get_postgresql_settings()
    return create_engine(settings.POSTGRES_URL)


def get_session_maker():
    engine = get_engine()
    return sessionmaker(bind=engine, autoflush=False, autocommit=False)
