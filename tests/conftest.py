# configuration for unit tests
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from fastapi.testclient import TestClient

# from app.auth.inter_service_auth import verify_auth_token
from models.user import UserModel
from settings import settings
from models import Base, get_db
from main import application


@pytest.fixture(scope="function")
def db_engine():
    engine = create_engine(settings.DATABASE.SQLALCHEMY_TEST_DATABASE_URL)
    if not database_exists(engine.url):
        print(engine.url)
        create_database(engine.url)

    Base.metadata.create_all(bind=engine)
    yield engine


@pytest.fixture(scope="function")
def db_session(db_engine):
    testing_session_factory = sessionmaker(
        autoflush=False, autocommit=False, bind=db_engine
    )
    try:
        session = testing_session_factory()
        yield session
    finally:
        clear_db(session)
        session.close()


@pytest.fixture(scope="function")
def client(db_session):
    application.dependency_overrides[get_db] = lambda: db_session

    with TestClient(application) as client:
        yield client


def clear_db(session):
    session.query(UserModel).delete()
    session.commit()
