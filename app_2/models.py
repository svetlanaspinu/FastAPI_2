# define the tables in python using ORM
# every models represent a table in the database

from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey#to create the column,
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

class Post(Base):
    #table name
    __tablename__ = "posts"

    # define the columns/ nullable=False - not allowed to be empty
    id = Column(Integer, primary_key=True, nullable=False)
    ttile = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="True", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

# connecting users tables and posts table in PgAdmin = setup ForeignKey
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # this tells sqlalchemy to fetch information based on the relationship
    owner = relationship("User")

# define a model that holds the user information - is a Postgres table
class User(Base): # Base is a require of sql model
    __tablename__ = 'users'
# creating the colums
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True) # unique=True - prevent 1 email to register twice
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


# model for the Votes table in pgadmin
class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True) # CASCADE - if you delete from one table is deleting from everywhere
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)


