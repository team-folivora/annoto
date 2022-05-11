"""
Module for integration tests
"""

from mod.tests.integration.conftest import ManagedTestClient


def test_ping(client: ManagedTestClient) -> None:
    """Test GET /ping"""
    client.authorize()
    response = client.get("/ping")
    assert response.status_code == 204
