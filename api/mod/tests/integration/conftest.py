"""Fixtures for integration tests."""
import pytest

AUTH_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJmdWxsbmFtZSI6IlByb2YuIERyLiBGb2xpdm9yYSIsImV4cGlyZXMiOjMyMjg1NzY2ODEuNjkxNjMxM30.feRiRVFJMpcrwjcVlh8A8QR7WribXOUdTxMh2crjRAQ"  # pylint: disable=line-too-long


@pytest.fixture
def authorization() -> str:
    """Returns a working value for the authorization header"""
    return f"Bearer {AUTH_TOKEN}"
