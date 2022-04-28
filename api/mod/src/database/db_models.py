"""
Defines the database models.
"""

import hashlib
import hmac
import os
from typing import Optional

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session

from mod.src.models.user import UserCreate

from .database import Base


class User(Base):
    """The basic user database model"""

    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, index=True)
    username: str = Column(String)
    email: str = Column(String, unique=True, index=True)
    hashed_password: bytes = Column(String)
    salt: bytes = Column(String)

    def __init__(self, username: str, email: str, password: str):
        self.username = username
        self.email = email
        self.set_password(password)

    @classmethod
    def create(cls, db: Session, user: UserCreate) -> "User":
        """Creates a new user and stores it in the database"""
        db_user = cls(user.username, user.email, user.password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @classmethod
    def get_by_email(cls, db: Session, email: str) -> Optional["User"]:
        """Get a user by email"""
        return db.query(cls).filter(cls.email == email).first()

    @classmethod
    def get_by_id(cls, db: Session, user_id: int) -> Optional["User"]:
        """Get a user by id"""
        return db.query(cls).filter(cls.id == user_id).first()

    def set_password(self, password: str) -> None:
        """Set the hashed password"""
        self.salt = os.urandom(16)
        self.hashed_password = hashlib.pbkdf2_hmac(
            "sha512", password.encode(), self.salt, 100000
        )

    def verify_password(self, password: str) -> bool:
        """Verify the password"""
        return hmac.compare_digest(
            self.hashed_password,
            hashlib.pbkdf2_hmac("sha512", password.encode(), self.salt, 100000),
        )

    def __repr__(self) -> str:
        return f"<User {self.username}>"
