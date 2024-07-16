# this file holds the hashing password code/ hashing logic
from passlib.context import CryptContext #first i installed pip install "passlib[bcrypt]" to hide the password from Postgres


#telling to passlib that we want to use the bcrypt as a hashing alghorithm 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)


# this function compares the hashing passwords
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)