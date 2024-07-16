                            # Contains path Operation of the Users


from .. import models, schemas, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter # (Response/status fro HTTPExceptions)
from sqlalchemy.orm import Session
from ..database import get_db

# creating a router object that holds the decorator and app to connect to fatsapi and replace with router
router = APIRouter(
    prefix="/users",
    tags=['Users']
)


# creating a path operations for new user to register to the API
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)): ## the email and password is stored in user

#hash the password that can be retrieve in user.password
# calling the pwd that contains the hash algorithm, attach the hash method, passing the user.password to hide the password
    hashed_password = utils.hash(user.password)
    #storing the hased password in user.password
    user.password = hashed_password
    new_user = models.User(**user.dict()) # create new user
    db.add(new_user) # added to database
    db.commit() # commit it to database
    db.refresh(new_user) #retrieve the data and store in new_user
    return new_user

# path operation to retrieve a post(to access someone profile/posts)
@router.get('/{id}',response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    # if user not found
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist.")

        # if user found return user
    return user
