import pytest
from app_2 import models


#creatinf a post for the test if a user want to like a vote twiece
@pytest.fixture()
def test_vote(test_posts, session, test_user):
    new_vote = models.Vote(post_id=test_posts[0].id, user_id=test_user['id'])
    session.add(new_vote)
    session.commit()


# success vote
def test_vote_on_post(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[0].id, "dir":1})
    res.status_code == 201

# test if a user want to like a ote twiece
def test_vote_twice_post(authorized_client, test_posts, test_vote):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[0].id, "dir":1})
    assert res.status_code == 409

# test deleting a vote
def test_delete_vote(authorized_client, test_posts, test_vote):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[0].id, "dir":0})
    assert res.status_code == 201

# testing a user that isnt authenticated cant vote
def test_vote_unauthorized_user(client, test_posts):
    res = client.post("/vote/", json={"post_id": test_posts[0].id, "dir":1})
    assert res.status_code == 401