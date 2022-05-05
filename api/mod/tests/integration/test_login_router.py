"""
Module for integration tests
"""

from fastapi.testclient import TestClient
from pytest_mock import MockerFixture
from sqlalchemy.orm import Session

from mod.src.database.db_models import DBUser


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
    response = client.get("/tasks", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200


def test_login_returns_correct_fullname(client: TestClient, db: Session) -> None:
    """Test POST /login"""
    response = client.post(
        "/login/",
        json={"email": "team@folivora.online", "password": "password"},
    )
    assert response.status_code == 200
    name = response.json()["fullname"]
    assert DBUser.get_by_email(db, email="team@folivora.online").fullname == name


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
    response = client.get("/tasks", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403


def test_login_is_required(client: TestClient) -> None:
    """Test POST /tasks"""
    response = client.get("/tasks")
    assert response.status_code == 403
