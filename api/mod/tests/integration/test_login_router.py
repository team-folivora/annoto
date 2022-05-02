"""
Module for integration tests
"""

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from mod.src.database import db_models
from mod.src.models import user


def test_login(client: TestClient, db: Session, user: user.UserCreate) -> None:
    """Test POST /login"""
    db_models.User.create(db=db, user=user)
    response = client.post(
        "/login/",
        json={"username": "AnnotoUser#1337", "password": "password"},
    )
    assert response.status_code == 204


def test_unknown_user_returns_400(client: TestClient) -> None:
    """Test POST /login raises HttpException 401"""
    response = client.post(
        "/login/",
        json={"username": "AnnotoUser#1337", "password": "wrong_password"},
    )
    assert response.status_code == 400


def test_invalid_password_returns_401(
    client: TestClient, db: Session, user: user.UserCreate
) -> None:
    """Test POST /login raises HttpException 401"""
    db_models.User.create(db=db, user=user)
    response = client.post(
        "/login/",
        json={"username": "AnnotoUser#1337", "password": "wrong_password"},
    )
    assert response.status_code == 401
