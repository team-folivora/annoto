"""
Module for integration tests
"""

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from mod.src.database import db_models
from mod.src.models import user


def test_get_user_returns_correct_user(client: TestClient, db: Session) -> None:
    """Test GET /users/1"""
    test_user = user.UserCreate(
        username="AnnotoUser#1337",
        password="password",
        email="annoto@team-folivora.com",
    )
    db_models.User.create(db=db, user=test_user)
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json()["username"] == test_user.username


def test_get_unknown_user_returns_404(client: TestClient) -> None:
    """Test GET /users/42"""
    response = client.get("/users/42")
    assert response.status_code == 404


def test_create_user_with_existing_email_returns_400(client: TestClient, db: Session) -> None:
    """Test POST /users/ with existing email"""
    test_user = user.UserCreate(
        username="AnnotoUser#1337",
        password="password",
        email="annoto@team-folivora.com",
    )
    db_models.User.create(db=db, user=test_user)
    response = client.post(
        "/users/",
        json=test_user.dict(),
    )
    assert response.status_code == 400


def test_create_user(client: TestClient, db: Session) -> None:
    """Test POST /users/ with new user"""
    test_user = user.UserCreate(
        username="AnnotoUser#1337",
        password="password",
        email="annoto@team-folivora.com",
    )
    response = client.post(
        "/users/",
        json=test_user.dict(),
    )
    assert response.status_code == 200
    created_user = db_models.User.get_by_email(db, email=test_user.email)
    assert created_user is not None
    assert (
        created_user.id
        == response.json()["id"]
    )
