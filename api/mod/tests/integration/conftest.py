"""Fixtures for integration tests."""
import pytest
from fastapi.testclient import TestClient
from mod.src.app import APP

AUTH_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJmdWxsbmFtZSI6IlByb2YuIERyLiBGb2xpdm9yYSIsImV4cGlyZXMiOjMyMjg1NzY2ODEuNjkxNjMxM30.feRiRVFJMpcrwjcVlh8A8QR7WribXOUdTxMh2crjRAQ"  # pylint: disable=line-too-long


class ManagedTestClient(TestClient):
    """Extended Test Client for integration tests to provide authorization capabilities."""

    def authorize(self) -> "ManagedTestClient":
        """Authorize the client."""

        self.headers.update({"Authorization": f"Bearer {AUTH_TOKEN}"})
        return self


@pytest.fixture()
def client() -> ManagedTestClient:
    """Get a client for testing the api"""

    return ManagedTestClient(APP)
