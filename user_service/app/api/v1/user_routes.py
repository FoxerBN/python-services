from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserCreate, UserRead, UserUpdate
from app.config.database import get_db
from app.service.user_service import create_user, get_user_by_username, get_all_users, delete_user, update_user

router = APIRouter()

@router.post("/user/add", response_model=UserRead)
def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(user, db)

@router.get("/user/getone", response_model=UserRead)
def get_user_route(username: str, db: Session = Depends(get_db)):
    return get_user_by_username(username, db)

@router.get("/user/getall", response_model=list[UserRead])
def get_all_users_route(db: Session = Depends(get_db)):
    return get_all_users(db)

@router.delete("/user/delete")
def delete_user_route(username: str, db: Session = Depends(get_db)):
    return delete_user(username, db)

@router.put("/user/update/{id}",response_model=UserRead)
def update_user_route(id: int, user: UserUpdate, db: Session = Depends(get_db)):
    return update_user(id, user, db)
