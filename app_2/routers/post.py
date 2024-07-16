                    # Contains path Operation of the Posts

from .. import models, schemas, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter # (Response/status fro HTTPExceptions)
from sqlalchemy.orm import Session
from ..database import get_db  
from typing import List, Optional #it improves code readability; helps in reducing runtime errors,         
from sqlalchemy import func # give action to function like count to count users in pgadmin - result 

router = APIRouter(
    prefix="/posts",
    tags=['Posts']  # connecting with the path from the @router, not to write /post everytime but only "/"
)


         # getting all posts - GET POSTS
@router.get("/", response_model=List[schemas.PostOut])   # the path operations / List - specify that we want a list for Respone
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit:int = 10, skip: int = 0, search: Optional[str] = ""):
    #making a query
    #cursor.execute("""SELECT * FROM posts""")
    # to run in postman
    #posts = cursor.fetchall()

   # posts = db.query(models.Post).filter(
        #models.Post.ttile.contains(search)).limit(limit).offset(skip).all() # to get/retrieve all post  /limit, skip - pagination
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter( 
            models.Post.ttile.contains(search)).limit(limit).offset(skip).all() #join to specify the join tables in sqlalchemy and the tables we want to join
   
    return posts



# testing the connection sqlalchemy with pgadmin/ if the code is connected with pgadmin Database
#@app.get("/sqlalchemy")
#def test_posts(db: Session = Depends(get_db)):
    #posts = db.query(models.Post).all()
    #return{"data": posts}



        # creating a Post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post) # the response_model - its the response output
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):  # the user_id Dependemce force a user to login before creating a post
    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,(post.title, post.content, post.published))
    #new_post = cursor.fetchone()
    #push the changes from Postman to PgAdmin
   # conn.commit()
    #print(**post.dict())

   

    new_post = models.Post(owner_id=current_user.id, **post.dict()) # create anew post
    db.add(new_post) # added to database
    db.commit() # commit it to database
    db.refresh(new_post) #retrieve the data and store in new_post
    return new_post

# telling the frond end what data do we expect:
# we want for a post request: title-str, content-str # we want user to send this information


        #retrieving/getting one individual post - GET ONE POST
@router.get("/{id}", response_model=schemas.PostOut) # the texr in te url/ id embeded in the url/ the id is a path parameter
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # THIS WAS THE SQL CODE/ cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),)) # daca nu pun , dupa (str(id)) - am eroare/ i am using the %s to store(hide) the data/ not to be vulnerable to sql injection
    #post = cursor.fetchone()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} was not found")
        #respone.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"post with id: {id} was not found"}
    return post



    # Delete a Post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT) 
def delete_post(id : int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

#COMMENT THE SQL CODE/ cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    #deleted_posts = cursor.fetchone()
    #find the index in the array that has required ID
    #my_posts.app.popo(index) - sa luam indexul
    #conn.commit()
    # to solve the 'NoneType' object cannot be interpreted as an integer error

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} cannot be found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")


# if the post exist to delete the post
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


        # UPDATE POST
@router.put("/{id}", response_model=schemas.Post)
def update_posts(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): # post: Post making use of the preexisting schema
    #find the index in the array that has required ID
    #my_posts.app.popo(index) - sa luam indexul

    #cursor.execute("""UPDATE posts SET ttile = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.ttile, post.content, post.published, str(id),))
    #updated_post = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    # to solve the 'NoneType' object cannot be interpreted as an integer error
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} cannot be found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")

    # if the post exist
    post_query.update(updated_post.dict(), synchronize_session=False) # passing the fields that we want to update as a dictionary
    db.commit()
    #post_dict = post.dict() # willl take the data store in Post and convertit to a dictionary
    #post_dict['id'] = id  # put the id inside the post.dict()
    #my_posts[index] = post_dict # passing the index of the updated id

    return post_query.first() # return the new_post

