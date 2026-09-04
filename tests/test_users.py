from jose import jwt
from app.config import settings
import pytest
from app import schemas



def test_root(client):
    res = client.get("/")
    assert res.json().get('message') == 'Bound mount'
    assert res.status_code == 200

def test_create_user(client):
    res = client.post("/users", json={"email": "hello@gmail.com", "password":"munna"})

    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello@gmail.com"
    assert res.status_code == 201

def test_login_user(client, test_user):
    res = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})

    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ("wrongemail@gmail.com", "munna", 403),
    ("hello@gmail.com", "wrongpass", 403),
    ("", "munna", 422),
    ("hello@gmail.com", "", 422)
])

def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post('/login', data={"username": email, "password": password})

    assert res.status_code == status_code
    if status_code == 403:
        assert res.json().get('detail') == "Invalid credentials"