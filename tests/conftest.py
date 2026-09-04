from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app
from app.config import settings
from app import models
from app.oauth2 import create_access_token

SQL_ALCHEMY_DATABASE_URL = f"postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}_test"

engine = create_engine(SQL_ALCHEMY_DATABASE_URL)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# TestSessionLocal is a factory function that creates a new Session object each time 
# it is called. It is used to create a new database session for each test function.

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine) # drop the tables in the database after the test function is executed
    Base.metadata.create_all(bind=engine) # create the tables in the database if they don't exist
    db = TestSessionLocal() # create a new database session
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
    yield TestClient(app) # yield the TestClient instance to be used in the test functions

@pytest.fixture
def test_user(client):
    user_data = {"email": "hello@gmail.com", "password": "munna"}
    res = client.post("/users", json=user_data)
    assert res.status_code == 201
    new_user = res.json() # convert the response to a JSON object and store it in the new_user variable
    new_user['password'] = user_data['password'] # add the password to the new_user dictionary so that it can be used in the test_login_user function
    return new_user # return the new_user dictionary so that it can be used in the test_login_user function

@pytest.fixture
def token(test_user):
    return create_access_token(data={"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user, session):
    posts_data = [
        {"title": "first title", "content": "first content", "owner_id": test_user['id']},
        {"title": "second title", "content": "second content", "owner_id": test_user['id']},
        {"title": "third title", "content": "third content", "owner_id": test_user['id']}
    ]
    session.add_all([models.Post(**post) for post in posts_data]) # add all the posts to the database
    session.commit() # commit the changes to the database
    return session.query(models.Post).all() # query the database for all the posts