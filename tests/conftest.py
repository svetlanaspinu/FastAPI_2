# this is a special file that pytets uses, it allows ti define fixture here
# any fixture defined in this fiel will automatically be accesible to any of the tets within this package, is package specific
# anythnink within the test package, and subpackage, will automatically have acces to this fixtures

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app_2.main import app
from app_2.oauth2 import create_access_token
from app_2.config import settings
from app_2.database import get_db, Base
import pytest
from app_2 import models


#           Creating a acode to taste the Database
# specify the connection string/ where is the database located
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

# create an engine that is responsible for sqlalchemy to connect to a Postgre Database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# this helps to talk with th database
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #this are defaul values from fastapi-sql website.and

# to create the tables for api_project2_testing in pgadmin
#Base.metadata.create_all(bind=engine)

#           a fixture runs before the testing code runs
# whrn finish a test is going to drop all the tables, delete the data, next time when run is going to creata tha tables again
# then will run the test using yield TestClient, then drop all the ytables again.
@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine) # delete table
    Base.metadata.create_all(bind=engine) #create table
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():

        try:
            yield session
        finally:
            session.close()
    # from fastapi testing a database
    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

# for tets when a user want to delete a post that isnt owns
@pytest.fixture
def test_user(client):
    user_data = {"email": "maria12@yahoo.com", "password": "password000"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


# test creating a user
@pytest.fixture
def test_user(client):
    user_data = {"email": "maria@yahoo.com", "password": "password000"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

# test user authentication
@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

# to get the authenticated user
@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client

# creating the post in the database
@pytest.fixture
def test_posts(test_user, session):
    posts_data = [{
        "ttile": "first title",
        "content": "first content",
        "owner_id": test_user['id']
    }, {
        "ttile": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
    }, {
        "ttile": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']
    },{
        "ttile": "for testing user",
        "content": "content",
        "owner_id": test_user['id']
    }]



    def create_post_model(post):
        #converting dictionary in post model
       return models.Post(**post)  # spread it
#converting the dictionary above to the format below (into a post models)- list format using map() function
    post_map = map(create_post_model, posts_data)
    # convert the map into list
    posts = list(post_map)
    session.add_all(posts)


# to add multiple entry into database = add.all()
   # session.add_all([models.Post(title="this is the title", content="this is the content", owner_id=test_user['id']),
        # models.Post(title="this is the 2nd title", content="this is the 2nd content", owner_id=test_user['id']),
     #models.Post(title="this is the 3rd title", content="this is the 3rd content", owner_id=test_user['id'])
       # ])

    session.commit()
    posts = session.query(models.Post).all()
    return posts