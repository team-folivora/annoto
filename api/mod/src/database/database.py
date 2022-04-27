"""
This module defines database config and access methods
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from mod.src.settings import SETTINGS

Base = declarative_base()

engine = create_engine(
    SETTINGS.database_url, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> sessionmaker:
    """Returns a database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
