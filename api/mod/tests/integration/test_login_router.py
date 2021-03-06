"""
Module for integration tests
"""

from pytest_mock import MockerFixture

from mod.tests.integration.conftest import ManagedTestClient


def test_login(client: ManagedTestClient) -> None:
    """Test POST /login"""
    response = client.post(
        "/login/",
        json={"email": "team@folivora.online", "password": "password"},
    )
    assert response.status_code == 200


def test_unknown_user_returns_401(client: ManagedTestClient) -> None:
    """Test POST /login raises HttpException 401"""
    response = client.post(
        "/login/",
        json={"email": "wrong-team@folivora.online", "password": "password"},
    )
    assert response.status_code == 401


def test_invalid_password_returns_401(client: ManagedTestClient) -> None:
    """Test POST /login raises HttpException 401"""
    response = client.post(
        "/login/",
        json={"email": "team@folivora.online", "password": "wrong_password"},
    )
    assert response.status_code == 401


def test_login_token_is_usable(client: ManagedTestClient) -> None:
    """Test POST /login"""
    response = client.post(
        "/login/",
        json={"email": "team@folivora.online", "password": "password"},
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    response = client.get("/ping", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 204


def test_login_token_expires(client: ManagedTestClient, mocker: MockerFixture) -> None:
    """Test POST /login"""
    mocker.patch("time.time", return_value=0)
    response = client.post(
        "/login/",
        json={"email": "team@folivora.online", "password": "password"},
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    mocker.patch("time.time", return_value=1e9)
    response = client.get("/ping", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403


def test_login_is_required(client: ManagedTestClient) -> None:
    """Test GET /ping"""
    response = client.get("/ping")
    assert response.status_code == 403
