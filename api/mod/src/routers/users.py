"""Routes for users"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from mod.src.database import db_models
from mod.src.database.database import get_db
from mod.src.models import user

ROUTER = APIRouter(
    prefix="/users",
    tags=["users"],
)


@ROUTER.get(
    "/{user_id}",
    response_model=user.User,
    responses={
        404: {"description": "User not found"},
    },
    operation_id="read_user",
)
def read_user(user_id: int, db: Session = Depends(get_db)) -> user.User:
    """Read a user by their ID"""
    db_user = db_models.User.get_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@ROUTER.post(
    "/",
    response_model=user.User,
    responses={
        400: {"description": "Email or username already registered"},
    },
    operation_id="create_user",
)
def create_user(user: user.UserCreate, db: Session = Depends(get_db)) -> user.User:
    """Create a user"""
    db_user = db_models.User.get_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = db_models.User.get_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return db_models.User.create(db, user=user)
