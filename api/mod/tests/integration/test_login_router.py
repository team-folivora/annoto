"""
Module for integration tests
"""

from fastapi.testclient import TestClient
from pytest_mock import MockerFixture


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


def test_login_token_is_usable(client: TestClient) -> None:
    """Test POST /login"""
    response = client.post(
        "/login/",
        json={"email": "team@folivora.online", "password": "password"},
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    response = client.get("/ping", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 204


def test_login_token_expires(client: TestClient, mocker: MockerFixture) -> None:
    """Test POST /login"""
    mocker.patch("time.time", lambda: 0)
    response = client.post(
        "/login/",
        json={"email": "team@folivora.online", "password": "password"},
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    mocker.patch("time.time", lambda: 1e9)
    response = client.get("/ping", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403


def test_login_is_required(client: TestClient) -> None:
    """Test GET /ping"""
    response = client.get("/ping")
    assert response.status_code == 403
