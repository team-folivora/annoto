from sqlalchemy.orm import Session
from . import models, schemas

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    hashed_password = user.password + "hash" # Create actually hashed password
    db_user = models.User(email = user.email, hashed_password = hashed_password, uername = user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db.user)
    return db_user

def get_user_by_email(db: Session, email: str) -> models.User:
    return db.query(models.User).filter(models.User.email == email).first()
