"""
Defines the database models.
"""

import hashlib
import hmac
import os
from typing import Optional

from sqlalchemy import Column, Integer, LargeBinary, String
from sqlalchemy.orm import Session

from mod.src.models.user import CreateUserRequest

from .database import Base


class DBUser(Base):
    """The basic user database model"""

    __tablename__ = "users"
    __hash_iterations__ = 100000

    id: int = Column(Integer, primary_key=True, unique=True, index=True, nullable=False)
    username: str = Column(String, unique=True, index=True, nullable=False)
    email: str = Column(String, unique=True, index=True, nullable=False)
    hashed_password: bytes = Column(LargeBinary, nullable=False)
    salt: bytes = Column(LargeBinary, nullable=False)

    @classmethod
    def with_password(cls, username: str, email: str, password: str) -> "DBUser":
        """Create a new user object and automatically hash the password"""
        user = cls()
        user.email = email
        user.username = username
        user.set_password(password)
        return user

    @classmethod
    def create(cls, db: Session, user: CreateUserRequest) -> "DBUser":
        """Creates a new user and stores it in the database"""
        db_user = cls.with_password(user.username, user.email, user.password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @classmethod
    def get_by_email(cls, db: Session, email: str) -> Optional["DBUser"]:
        """Get a user by email"""
        return db.query(cls).filter(cls.email == email).first()

    @classmethod
    def get_by_username(cls, db: Session, username: str) -> Optional["DBUser"]:
        """Get a user by username"""
        return db.query(cls).filter(cls.username == username).first()

    @classmethod
    def get_by_id(cls, db: Session, user_id: int) -> Optional["DBUser"]:
        """Get a user by id"""
        return db.query(cls).filter(cls.id == user_id).first()

    def set_password(self, password: str) -> None:
        """Set the hashed password"""
        self.salt = os.urandom(16)
        self.hashed_password = hashlib.pbkdf2_hmac(
            "sha512", password.encode(), self.salt, self.__hash_iterations__
        )

    def verify_password(self, password: str) -> bool:
        """Verify the password"""
        return hmac.compare_digest(
            self.hashed_password,
            hashlib.pbkdf2_hmac(
                "sha512", password.encode(), self.salt, self.__hash_iterations__
            ),
        )

    def __repr__(self) -> str:
        return f"<User {self.username}>"
