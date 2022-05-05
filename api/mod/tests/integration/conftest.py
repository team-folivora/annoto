"""Fixtures for integration tests."""
import pytest

AUTH_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJleHBpcmVzIjozMjI4NDc5OTIwLjI4MzI0NX0.0tL-qwtDvIV-b7pR1fwcwtUIcT3kjt43vEFiVKsN_9I"  # pylint: disable=line-too-long


@pytest.fixture
def authorization() -> str:
    """Returns a working value for the authorization header"""
    return f"Bearer {AUTH_TOKEN}"
