from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserCreate, UserUpdate
from app.models.user_model import User
from app.config.database import get_db
import hashlib

def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user in the database.
    Args:
        user (UserCreate): The user data to create.
        db (Session, optional): The database session. Defaults to Depends(get_db).
    Raises:
        HTTPException: If the username already exists.
    Returns:
        User: The created user object.
    """
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed = hashlib.sha256(user.password.encode()).hexdigest()
    db_user = User(username=user.username, hashed_password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(username: str, db: Session = Depends(get_db)):
    """Retrieve a user by username.
    Args:
        username (str): The username to search for.
        db (Session, optional): The database session. Defaults to Depends(get_db).
    Returns:
        User: The user object if found, otherwise None.
    """
    return db.query(User).filter(User.username == username).first()

def get_all_users(db: Session = Depends(get_db)):
    """Retrieve all users from the database.
    Args:
        db (Session, optional): The database session. Defaults to Depends(get_db).
    Returns:
        List[User]: A list of all user objects.
    """
    return db.query(User).all()

def delete_user(username: str, db: Session = Depends(get_db)):
    """Delete a user by username.
    Args:
        username (str): The username of the user to delete.
        db (Session, optional): The database session. Defaults to Depends(get_db).
    Raises:
        HTTPException: If the user does not exist.
    """
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"detail": "User deleted successfully"}


def update_user(id: int, user: UserUpdate, db: Session = Depends(get_db)):
    """Update a user by id.
    Args:
        id (int): The id of the user to update.
        user (UserUpdate): The updated user data with optional username and/or password.
        db (Session, optional): The database session. Defaults to Depends(get_db).
    Raises:
        HTTPException: If the user does not exist.
    Returns:
        User: The updated user object.
    """
    existing_user = db.query(User).filter(User.id == id).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update username if provided
    if user.username is not None:
        existing_user.username = user.username #type: ignore

    # Update password if provided
    if user.password is not None:
        existing_user.hashed_password = hashlib.sha256(user.password.encode()).hexdigest()#type: ignore

    db.commit()
    db.refresh(existing_user)
    return existing_user