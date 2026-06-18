from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import postgresql_settings

engine = create_engine(postgresql_settings.POSTGRES_URL)
postgresql_session_maker = sessionmaker(bind=engine)
