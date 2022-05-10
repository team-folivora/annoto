from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker

from mod.src.settings import SETTINGS
from scripts.config import meta, session


def empty_db():
    """Emtpies all rows in all tables except for the alembic version"""

    for table in reversed(meta.sorted_tables):
        if table.name != "alembic_version":
            session.execute(table.delete())
    session.commit()


if __name__ == "__main__":
    empty_db()
