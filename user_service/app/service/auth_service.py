from fastapi import HTTPException, Response
from sqlalchemy.orm import Session
from app.models.user_model import User
from app.utils.auth_tokens import create_access_token

COOKIE_NAME = "access_token"
COOKIE_PATH = "/"
SAMESITE = "lax"

def login_user(username: str, password: str, response: Response, db: Session):
    """Login a user and set a cookie with the access token."""
    user = db.query(User).filter(User.username == username).first()
    if not user or not user.check_password(password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    token = create_access_token(user.username, user.id)
    response.set_cookie(
        key=COOKIE_NAME,
        value=token,
        httponly=True,
        samesite=SAMESITE,
        path=COOKIE_PATH,
    )
    return {"message": "Login successful"}

def logout_user(response: Response):
    """Logout a user and delete the cookie."""
    response.delete_cookie(
        key=COOKIE_NAME,
        path=COOKIE_PATH,
    )
    return {"message": "Logout successful"}
