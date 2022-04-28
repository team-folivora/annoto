"""
Module for unit tests
"""


import hashlib

from mod.src.database import db_models

def test_hash_new_password() -> None:
    """Test if new hash for password is generated correctly"""
    password = "password"
    user: db_models.User = db_models.User("AnnotoUser", "email", password)
    test_hash = hashlib.pbkdf2_hmac("sha512", password.encode(), user.salt, 100000)
    assert user.hashed_password == test_hash


def test_hash_check() -> None:
    """Test the password-check function"""
    password = "password"
    user: db_models.User = db_models.User("AnnotoUser", "email", password)
    assert user.verify_password(password)
    assert not user.verify_password("wrong_password")
