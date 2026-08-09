from app.database.postgresql import get_session_maker


def get_db():
    SessionLocal = get_session_maker()
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
