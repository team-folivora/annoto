"""
Module for integration tests
"""

from fastapi.testclient import TestClient


def test_login(client: TestClient) -> None:
    """Test POST /login"""
    response = client.post(
        "/login/",
        json={"username": "AnnotoUser#1337", "password": "test1234"},
    )
    assert response.status_code == 204


def test_invalid_login_returns_401(client: TestClient) -> None:
    """Test POST /login raises HttpException 401"""
    response = client.post(
        "/login/",
        json={"username": "AnnotoUser#1337", "password": "wrong_password"},
    )
    assert response.status_code == 401
