from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app

from app.config import settings
from app.database import get_db
from app.database import Base
from app.oauth2 import create_access_token
from app import models
from alembic import command



SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'


engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():

        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user2(client):
    user_data = {"email": "kat@gmail.com",
                 "password": "password"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def test_user(client):
    user_data = {"email": "ethan@gmail.com",
                 "password": "password"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client


@pytest.fixture
def test_titles(test_user, session, test_user2):
    titles_data = [{
        "title": "Dick Johnson Is Dead",
        "show_id": "s1",
        "type":"Movie",
        "release_year":"2020",
        "listed_in":"Documentaries",
        "description":"As her father nears the end of his life, filmmaker Kirsten Johnson stages his death in inventive and comical ways to help them both face the inevitable.",
        "owner_id": test_user['id']
    }, {
        "title": "Blood & Water",
        "show_id": "s2",
        "type":"TV Show",
        "release_year":"2021",
        "listed_in":"International TV Shows, TV Dramas, TV Mysteries",
        "description":"After crossing paths at a party, a Cape Town teen sets out to prove whether a private-school swimming star is her sister who was abducted at birth.",
        "owner_id": test_user['id']
    },
        {
        "title": "Ganglands",
        "show_id": "s3",
        "type":"TV Show",
        "release_year":"2021",
        "listed_in":"Crime TV Shows, International TV Shows, TV Action & Adventure",
        "description":"To protect his family from a powerful drug lord, skilled thief Mehdi and his expert team of robbers are pulled into a violent and deadly turf war.",
        "owner_id": test_user['id']
    }, {
        "title": "Jailbirds New Orleans",
        "show_id": "s4",
        "type":"TV Show",
        "release_year":"2021",
        "listed_in":"Docuseries, Reality TV",
        "description":"Feuds, flirtations and toilet talk go down among the incarcerated women at the Orleans Justice Center in New Orleans on this gritty reality series.",
        "owner_id": test_user['id']
    }]

    def create_title_model(title):
        return models.Title(**title)

    title_map = map(create_title_model, titles_data)
    titles = list(title_map)

    session.add_all(titles)
    session.commit()

    titles = session.query(models.Title).all()
    return titles
