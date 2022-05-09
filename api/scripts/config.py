from pathlib import Path

from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker

from mod.src.settings import SETTINGS

file_path = Path.cwd().joinpath("mod").joinpath("fixtures").joinpath("test_data.json")

if not file_path.exists():
    print("File does not exist")
    exit(1)

engine = create_engine(SETTINGS.database_url, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

meta = MetaData()
meta.reflect(bind=engine)