from app.database.postgresql import postgresql_session_maker


def get_db():
    session = postgresql_session_maker()
    try:
        yield session
    finally:
        session.close()
