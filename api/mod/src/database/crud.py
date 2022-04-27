"""
This module holds functions to perform CRUD operations on the database
"""

from typing import Optional
from sqlalchemy.orm import Session
from mod.src.database.db_models import hash_new_password
from mod.src.database import db_models
from mod.src.models import user


def create_user(db: Session, user: user.UserCreate) -> db_models.User:
    """Create a user from the specified data"""
    salt, hashed_password = hash_new_password(user.password)
    db_user = db_models.User(
        email=user.email,
        hashed_password=hashed_password,
        username=user.username,
        salt=salt,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str) -> Optional[db_models.User]:
    """Get a user by their email"""
    return db.query(db_models.User).filter(db_models.User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[db_models.User]:
    """Get a user by their id"""
    return db.query(db_models.User).filter(db_models.User.id == user_id).first()
