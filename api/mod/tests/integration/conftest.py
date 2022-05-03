import pytest

from mod.src.models.user import CreateUserRequest


@pytest.fixture
def user() -> CreateUserRequest:
    """Creates a basic Annotation"""
    return CreateUserRequest(
        username="AnnotoUser#1337",
        password="password",
        email="annoto@team-folivora.com",
    )
