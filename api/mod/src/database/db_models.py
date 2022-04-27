"""
Defines the database models.
"""

import hashlib
import hmac
import os
from typing import Tuple

from sqlalchemy import Column, Integer, String

from .database import Base


class User(Base):
    """The basic user database model"""

    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, index=True)
    username: str = Column(String)
    email: str = Column(String, unique=True, index=True)
    hashed_password: str = Column(String)
    salt: str = Column(String)


# "Inspired" by https://stackoverflow.com/questions/9594125/salt-and-hash-a-password-in-python
def hash_new_password(password: str) -> Tuple[bytes, bytes]:
    """
    Hash the provided password with a randomly-generated salt and return the
    salt and hash to store in the database.
    """
    salt = os.urandom(16)
    pw_hash = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)
    return salt, pw_hash


def is_correct_password(salt: bytes, pw_hash: bytes, password: str) -> bool:
    """
    Given a previously-stored salt and hash, and a password provided by a user
    trying to log in, check whether the password is correct.
    """
    return hmac.compare_digest(
        pw_hash, hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)
    )
