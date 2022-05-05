"""
Module for integration tests
"""

from fastapi.testclient import TestClient


def test_ping(client: TestClient, authorization: str) -> None:
    """Test GET /ping"""
    response = client.get("/ping", headers={"Authorization": authorization})
    assert response.status_code == 204
