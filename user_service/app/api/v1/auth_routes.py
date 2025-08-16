from fastapi import APIRouter, Depends, Response, Request, HTTPException
from app.schemas.user_schema import LoginBody
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.service.auth_service import login_user, logout_user

router = APIRouter(prefix="/user", tags=["auth"])

@router.post("/login")
def login(body: LoginBody, response: Response, db: Session = Depends(get_db)):
    return login_user(body.username, body.password, response, db)

@router.post("/logout")
def logout(response: Response):
    return logout_user(response)

@router.get("/whoami")
def whoami(request: Request):
    if not getattr(request.state, "username", None):
        raise HTTPException(status_code=401, detail="Not authenticated")
    return {"username": request.state.username}