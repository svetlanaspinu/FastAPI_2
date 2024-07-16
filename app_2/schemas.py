# The schema models define the structure of a request & response. This ensure that when a user wants to create a post the request will
# only go through if it has a "title" and "content" in the body

from pydantic import BaseModel, EmailStr  #to create the schema
from datetime import datetime
from typing import Optional
from pydantic.types import conint


# Define a Class that show hiw a Post shoul look like
class Post(BaseModel): #creating the schme passing BaseModel
    ttile: str
    content: str
    published: bool = True # if a user dont provide a value is set to true - to show the date and time
    


#class CreatePost(BaseModel):
    #ttile: str
    #content: str
    #published: bool = True

#class UpdatePost(BaseModel):
    #published: bool = True

# this class holds the CreatePost and UpdatePost in ine class
class PostBase(BaseModel):
    ttile: str
    content: str
    published: bool = True # is optional if i dont provide one is true
   

#extend class PostBase by default will inherit the PostBase fileds
class PostCreate(PostBase) :
    pass  # it will accept whatever PostBase is

# creating the shape of the model when i sent back the user to the client that requested; and hiding his password in postman
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
# pydantic only works with dictionary, not with sql model. the from_attributes convert the sql model to be an pydantic model
    class Config:
        from_attributes = True

# aici specific ce data vreau sa fie send, si sunt in control la ce categorie de informatie pot avea acces
 # creating the response model
class Post(BaseModel):
    # sending back the content below
    id: int
    ttile: str
    content: str
    published: bool
    created_at: datetime
    owner_id: int
    owner: UserOut

# pydantic only works with dictionary, not with sql model. the from_attributes convert the sql model to be an pydantic model
    class Config:
        from_attributes = True

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        from_attributes = True

# creatimg the schemas for the user
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    

# creating user login using jwt token authentoication
class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True

# schemas for the Token
class Token(BaseModel):
    access_token: str
    token_type: str

# schema for the token data embede in access token
class TokenData(BaseModel):
    id: Optional[str] = None

# schema for voting
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)  # direction: anythig less=1 it will gonna be allowed





