"""
Module for unit tests
"""


from mod.src.models.user import CreateUserRequest
from mod.src.database.db_models import DBUser


def test_hash_new_password(mocker) -> None:
    """Test if new hash for password is generated correctly"""
    salt: bytes = b"salt"
    mocker.patch("os.urandom", return_value=salt)
    password = "password"
    test_hash = b'\xf5\xd1p"\xc9j\xf4l\n\x1d\xc4\x9aX\xbb\xe6T\xa2\x8e\x98\x10H\x83\xe4\xafM\xe9t\xcd\xa2\xc7A"\xdd\x08/A\x05\xa9?\xc8\x06\x92\xcaN\xb1\xa7\x84\xcf\xed\xa8\x1b\xfa\xa3?Q\x92\xcc\x91C\xd8\x18\xbdu\x81'
    user: DBUser = DBUser.from_create_request(
        CreateUserRequest(
            fullname="Prof. Dr. Folivora",
            email="team@folivora.online",
            password=password,
        )
    )
    assert user.hashed_password == test_hash


def test_hash_check() -> None:
    """Test the password-check function"""
    password = "password"
    user: DBUser = DBUser.from_create_request(
        CreateUserRequest(
            fullname="Prof. Dr. Folivora",
            email="team@folivora.online",
            password=password,
        )
    )
    assert user.verify_password(password)
    assert not user.verify_password("wrong_password")
