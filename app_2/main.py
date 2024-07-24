
# after creating the venv using py -3 -m venv venv we have to insatll API-pip install fastapi[all]
from fastapi import FastAPI # Response, status, HTTPException, Depends # (Response/status fro HTTPExceptions)
from fastapi.middleware.cors import CORSMiddleware# to access the api from difreent web browser
from . import models # schemas, utils
from .database import engine
from .routers import post, user, auth, vote
from .config import settings
#from fastapi.params import Body #to connect with body from Postman
#from pydantic import BaseModel  #to create the schema
#from typing import Optional, List #it improves code readability; helps in reducing runtime errors,
#from random import randrange #returns a randomly selected element from the specified range
#from sqlalchemy.orm import Session


#models.Base.metadata.create_all(bind=engine) # to connect with sqlaclhemy in postgres
# create an instance of FasAPI
app = FastAPI()

#for allow_origins to access the api [http://www.google.com]
origins = ["*"] # all the origins
#from fastapi corsmidleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, #what domains can talk with the api
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# connecting with the file routers that containes post/user file
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

# path operation
@app.get("/") # HTTP method .get
def root():
    return {"message": "Hello World! Succesfully deployed CI/CD pipeline"}


#teh array for the output
 # everytime we save a piece of information with databases, teh databases will create a unique identifier(id)
#my_posts = [{"ttile": "ttile of post 1", "content": "content of post 1", "id": 1}, 
   # {"ttile": "favorite foods", "content": "i like pizza", "id": 2}] 

# create the function to find the post by an id
#def find_post(id):
# iterate over my_posts, p is the post that we are iterate over
    #for p in my_posts:
       # if p["id"] == id: # the post has an id wich equals the ID that was passed into the function
            #return p # return that specific posts

#function to find the ID for the deleting Post
#def find_index_post(id): # (id) - passing the id we are interesting in 
# iterate over the array "i(index), p(post)" and grabbing the specifinc index that we are iterate over - using enumerate(my_posts), using my_post - to get the acces to the post(p) that we are iterating over and index(i)
    #for i, p in enumerate(my_posts):
# it will give us the index of the dictionary with the specific id / ... dupa aceasta ma duc inapoi jos la Delete a Post section
       # if p['id'] == id:
          #  return i #it will give us the index of the dictionary wuth the specific ID/ the dictionary is the my_posts-list

# using uvicorn library to run the api in terminal - uvicorn main:app --reload

# testing the HTTP methods on browser after that moving to Postman
#the decorator make the function to act like an API; turns the function into a path operation

