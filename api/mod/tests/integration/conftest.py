"""Fixtures for integration tests."""
import pytest

from mod.src.models.user import CreateUserRequest


@pytest.fixture
def user() -> CreateUserRequest:
    """Creates a basic Annotation"""
    return CreateUserRequest(
        fullname="Prof. Dr. Folivora",
        password="password",
        email="team@folivora.online",
    )
