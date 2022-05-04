"""
Module for integration tests
"""

from fastapi.testclient import TestClient


def test_login(client: TestClient) -> None:
    """Test POST /login"""
    response = client.post(
        "/login/",
        json={"email": "team@folivora.online", "password": "password"},
    )
    assert response.status_code == 200


def test_unknown_user_returns_401(client: TestClient) -> None:
    """Test POST /login raises HttpException 401"""
    response = client.post(
        "/login/",
        json={"email": "wrong-team@folivora.online", "password": "password"},
    )
    assert response.status_code == 401


def test_invalid_password_returns_401(client: TestClient) -> None:
    """Test POST /login raises HttpException 401"""
    response = client.post(
        "/login/",
        json={"email": "team@folivora.online", "password": "wrong_password"},
    )
    assert response.status_code == 401
