"""Routes for users"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from mod.src.database import db_models
from mod.src.database.database import get_db as DB
from mod.src.models.user import CreateUserRequest, UserResponse

ROUTER = APIRouter(
    prefix="/users",
    tags=["users"],
)


@ROUTER.get(
    "/{user_id}",
    response_model=UserResponse,
    responses={
        404: {"description": "User not found"},
    },
    operation_id="read_user",
)
def read_user(user_id: int, db: Session = Depends(DB)) -> UserResponse:
    """Read a user by their ID"""
    db_user = db_models.DBUser.get_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@ROUTER.post(
    "/",
    response_model=UserResponse,
    responses={
        400: {"description": "Email or username already registered"},
    },
    operation_id="create_user",
)
def create_user(user: CreateUserRequest, db: Session = Depends(DB)) -> UserResponse:
    """Create a user"""
    db_user = db_models.DBUser.get_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = db_models.DBUser.get_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return db_models.DBUser.create(db, user=user)
