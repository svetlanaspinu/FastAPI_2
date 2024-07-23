
import pytest
from app_2 import schemas

# autentication during testing
# testin Getting all posts
def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    def validate(post):
        return schemas.PostOut(**post)
    posts_map = map(validate, res.json())
    posts_list = list(posts_map)

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200

# testing an unauthenticated user is not able to retrieve the posts
def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401

# getting unauthorized user one post
def test_unauthorized_user_get_ine_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

# test post with od that dosent exist
def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/90")
    assert res.status_code == 404 

# test retrieve a valid post
def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.ttile == test_posts[0].ttile

# test creating a post
@pytest.mark.parametrize("ttile, content, published", [("this is the new ttile", "this is the new content", True),
    ("this is the 2nd new ttile", "this is the 2nd new content", False),
    ("this is the 3rd new ttile", "this is the 3rd new content", True)

]) # to test multiple value
def test_create_post(authorized_client, test_user, test_posts, ttile, content, published):
    res  = authorized_client.post("/posts/", json={"ttile": ttile, "content": content, "published": published})

    create_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert create_post.ttile == ttile
    assert create_post.content == content
    assert create_post.published == published
    assert create_post.owner_id == test_user['id']

# test if a user is not logged in 
def test_unauthorized_user_create_post(client, test_posts):
   res  = client.post("/posts/", json={"ttile": "title about my job", "content": "teh contet about my job"})
   assert res.status_code == 401

#unauthorized user trying to delete a post
def test_unauthorized_user_delete_Post(client, test_user, test_posts):
    res  = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

# test valid deletion
def test_delete_post_success(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204

# testing update a post
def test_update_post(authorized_client, test_posts, test_user):
    data = {
        "ttile": "update jobs",
        "content": "update content",
        "id": test_posts[0].id
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    update_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert update_post.ttile == data['ttile']
    assert update_post.content == data['content']


def test_unauthorized_user_update_Post(client, test_user, test_posts):
    res  = client.put(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401