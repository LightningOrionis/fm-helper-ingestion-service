from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import POSTGRES_SETTINGS

engine = create_engine(POSTGRES_SETTINGS.POSTGRES_URL)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)
