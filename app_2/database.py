                    # this file holds the database connection

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2 # connecting wirh the database PgAdmin
from psycopg2.extras import RealDictCursor # to connect with the columns of the database
import time # to stop the break in While loop
from .config import settings


# specify the connection string/ where is the database located
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# create an engine that is responsible for sqlalchemy to connect to a Postgre Database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# this helps to talk with th database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #this are defaul values from fastapi-sql website.and

Base = declarative_base()

# this function connects with the database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    



                # This connect database using Postgres - psycopg, after i have connected using sqlalchemy, this code is just for refernce.
                # all the While loop code can be commented. is not in use
# using a while loop to runt in case of incorrect password to connect the database..so to run tuntil is connected.
#while True:
    # connecting with the database:
    #try: 
        #conn = psycopg2.connect(host='localhost', database='api_project2', user='postgres', password='password456', cursor_factory=RealDictCursor)  
    # calling teh cursor method to execute sql statements
        #cursor = conn.cursor()
# if succesfully conect print the text
        #print("Database connection was succesfull created!")

        #if succesfully connected break the while loop
        #break

    # if not
    #except Exception as error: #the error store in variable error
        #print("Connecting to database failed!")
        #print("The error was: ", error)
        # set 3 sec before to output that the database was succesfully connected or not
        #time.sleep(3)

