"""
This module defines database config and access methods
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from mod.src.settings import SETTINGS

Base = declarative_base()

engine = create_engine(SETTINGS.database_url, connect_args=SETTINGS.engine_connect_args)
SessionLocal = sessionmaker(bind=engine)


def get_db() -> sessionmaker:
    """Returns a database session"""
    with SessionLocal() as session:
        yield session
