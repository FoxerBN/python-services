# tests/unit/test_user_service.py
import hashlib
import time
import pytest
from starlette.responses import Response
from fastapi import HTTPException
from app.service.auth_service import login_user, logout_user
from app.service.user_service import (
    create_user,
    get_user_by_username,
    get_all_users,
    delete_user,
    update_user,
)
from app.schemas.user_schema import UserCreate, UserUpdate, UserRead
from app.models.user_model import User

# create_user
def test_create_user_creates_and_hashes_password(db):
    data = UserCreate(username="ana", password="secret")
    u = create_user(data, db=db)
    assert isinstance(u, User)
    assert u.username == "ana"
    assert u.hashed_password != "secret"
    assert u.hashed_password == hashlib.sha256("secret".encode()).hexdigest()

def test_create_user_duplicate_raises(db, user_factory):
    user_factory("john", "pw")
    with pytest.raises(HTTPException) as ex:
        create_user(UserCreate(username="john", password="x"), db=db)
    assert ex.value.status_code == 400
    assert "exists" in ex.value.detail.lower()

# get_user_by_username / get_all_users
def test_get_user_by_username_returns_user(db, user_factory):
    user_factory("mila", "pw")
    found = get_user_by_username("mila", db=db)
    assert found is not None
    assert found.username == "mila"

def test_get_all_users_returns_list(db, user_factory):
    user_factory("a", "1")
    user_factory("b", "2")
    users = get_all_users(db=db)
    assert isinstance(users, list)
    assert {u.username for u in users} >= {"a", "b"}

# delete_user
def test_delete_user_deletes_existing(db, user_factory):
    user_factory("zara", "pw")
    res = delete_user("zara", db=db)
    assert res["detail"].startswith("User deleted")
    assert get_user_by_username("zara", db=db) is None

def test_delete_user_missing_raises_404(db):
    with pytest.raises(HTTPException) as ex:
        delete_user("ghost", db=db)
    assert ex.value.status_code == 404

# update_user
def test_update_user_updates_username_and_password(db, user_factory):
    u = user_factory("oldname", "oldpw")
    updated = update_user(
        id=u.id,
        user=UserUpdate(username="newname", password="newpw"),
        db=db,
    )
    assert updated.username == "newname"
    assert updated.hashed_password == hashlib.sha256("newpw".encode()).hexdigest()

def test_update_user_missing_raises_404(db):
    with pytest.raises(HTTPException) as ex:
        update_user(id=9999, user=UserUpdate(username="x"), db=db)
    assert ex.value.status_code == 404

# auth: login / logout
def test_login_user_success_sets_cookie_and_returns_message(monkeypatch, db, user_factory):
    u = user_factory("cookieuser", "pw123")
    assert u.check_password("pw123") is True

    def fake_create_access_token(username, user_id):
        assert username == "cookieuser"
        assert user_id == u.id
        return "FAKE-TOKEN"

    monkeypatch.setattr(
        "app.service.auth_service.create_access_token",
        fake_create_access_token,
    )

    response = Response()
    result = login_user(username="cookieuser", password="pw123", response=response, db=db)

    cookies = response.headers.get("set-cookie", "")
    assert "access_token=FAKE-TOKEN" in cookies
    assert "; HttpOnly" in cookies
    assert result["message"] == "Login successful"

def test_login_user_wrong_credentials_raise_401(db, user_factory):
    user_factory("bob", "rightpw")
    response = Response()
    with pytest.raises(HTTPException) as ex:
        login_user(username="bob", password="wrongpw", response=response, db=db)
    assert ex.value.status_code == 401

def test_logout_user_deletes_cookie():
    response = Response()
    res = logout_user(response)
    cookies = response.headers.get("set-cookie", "")
    assert "access_token=" in cookies and "Max-Age=0" in cookies
    assert res["message"] == "Logout successful"

# model: User
def test_user_model_check_password(db, user_factory):
    u = user_factory("tester", "mypw")
    assert u.check_password("mypw") is True
    assert u.check_password("wrong") is False

def test_user_model_timestamps(db, user_factory):
    u = user_factory("stampuser", "pw")
    assert u.created_at is not None
    assert u.updated_at is not None
    original_updated = u.updated_at

    # Force an update to trigger onupdate
    time.sleep(0.5)  # increase chance updated_at changes (second-level granularity)
    u.hashed_password = hashlib.sha256("newpw".encode()).hexdigest()
    db.commit()
    db.refresh(u)

    assert u.updated_at >= u.created_at
    assert u.updated_at >= original_updated

# schemas
def test_user_create_schema():
    data = UserCreate(username="neo", password="matrix")
    assert data.username == "neo"
    assert data.password == "matrix"

def test_user_update_schema_optional_fields():
    upd = UserUpdate()
    assert upd.username is None
    assert upd.password is None
    upd2 = UserUpdate(username="trinity")
    assert upd2.username == "trinity"
    assert upd2.password is None

def test_user_read_schema():
    from datetime import datetime
    now = datetime.utcnow()
    read = UserRead(id=1, username="smith", created_at=now, updated_at=now)
    assert read.id == 1
    assert read.username == "smith"
    assert read.created_at == now
    assert read.updated_at == now
