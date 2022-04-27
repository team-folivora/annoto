"""
Module for unit tests
"""


from mod.src.database import db_models
import hashlib
import os


def test_hash_new_password() -> None:
    """Test if new hash for password is generated correctly"""
    password = "password"
    salt, pw_hash = db_models.hash_new_password(password)
    test_hash = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)
    assert pw_hash == test_hash


def test_hash_check() -> None:
    """Test the password-check function"""
    password = "password"
    salt = os.urandom(16)
    pw_hash = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)
    assert db_models.is_correct_password(salt, pw_hash, password)
    assert not db_models.is_correct_password(salt, pw_hash, "wrong_password")
