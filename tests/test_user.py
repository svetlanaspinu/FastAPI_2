from app_2 import schemas
from .test_database import client, session
import pytest
from jose import jwt
from app_2.config import settings


#def test_root(client):
    #res = client.get("/")
    #print(res) # for passed/failed output
    #print(res.json().get('message')) # output Hello World from main.py file
    #assert res.json().get('message') == 'Hello World!!!!!'
    #assert res.status_code == 200




# testing create a user
def test_create_user(client):
    res = client.post("/users/", json={"email": "lala@yahoo.com", "password": "password456"}) # res=response, json={}-to send data in the body
    # for the information above in shemas.py for create user it request email+password
    
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "lala@yahoo.com"
    assert res.status_code == 201

#test login user
def test_login_user(client, test_user):
    res = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})
    login_res = schemas.Token(**res.json())
    # validate the token
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


#with the parametrize tetsing the incorect email, password, status code
@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password456', 403),
    ('maria@yahoo.com', 'password099', 403),
    (None, 'password111', 422)
])
#testing a failed login
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})

    assert res.status_code == status_code # instead of status code i can add password or email to test all the variable

    #assert res.json().get('detail') == 'Invalid Credentials'




