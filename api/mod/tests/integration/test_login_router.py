"""
Module for integration tests
"""

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from mod.src.database.db_models import DBUser
from mod.src.models.user import CreateUserRequest


def test_login(client: TestClient, db: Session, user: CreateUserRequest) -> None:
    """Test POST /login"""
    DBUser.create(db=db, user=user)
    response = client.post(
        "/login/",
        json={"email": "team@folivora.online", "password": "password"},
    )
    assert response.status_code == 204


def test_unknown_user_returns_401(client: TestClient) -> None:
    """Test POST /login raises HttpException 401"""
    response = client.post(
        "/login/",
        json={"email": "team@folivora.online", "password": "wrong_password"},
    )
    assert response.status_code == 401


def test_invalid_password_returns_401(
    client: TestClient, db: Session, user: CreateUserRequest
) -> None:
    """Test POST /login raises HttpException 401"""
    DBUser.create(db=db, user=user)
    response = client.post(
        "/login/",
        json={"email": "team@folivora.online", "password": "wrong_password"},
    )
    assert response.status_code == 401
