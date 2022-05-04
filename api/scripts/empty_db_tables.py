from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker

from mod.src.settings import SETTINGS


def empty_db():
    """Emtpies all rows in all tables except for the alembic version"""
    engine = create_engine(
        SETTINGS.database_url, connect_args={"check_same_thread": False}
    )

    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    meta = MetaData()
    meta.reflect(bind=engine)

    for table in reversed(meta.sorted_tables):
        if table.name != "alembic_version":
            print(table)
            session.execute(table.delete())
    session.commit()
