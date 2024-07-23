from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app_2.main import app

from app_2.config import settings
from app_2.database import get_db, Base
import pytest


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