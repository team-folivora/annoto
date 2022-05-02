import json
from pathlib import Path
from sqlalchemy import MetaData, create_engine
from mod.src.settings import SETTINGS
from sqlalchemy.orm import sessionmaker
from mod.src.database import database, db_models

file_path = Path.cwd().joinpath("mod").joinpath("fixtures").joinpath("test_data.json")

if not file_path.exists():
    print("File does not exist")
    exit(1)

def get_class_by_tablename(tablename):
    base = database.Base

    for mapper in base.registry.mappers:
        if mapper.class_.__tablename__ == tablename:
            return mapper.class_


class BytesDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, dct):
        if "hashed_password" in dct:
            dct["hashed_password"] = bytes.fromhex(dct["hashed_password"])
            dct["salt"] = bytes.fromhex(dct["salt"])
            return dct
        return dct

engine = create_engine(SETTINGS.database_url, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

with open(file_path) as f:
    data = f.read()
    jsondata = json.loads(data, cls=BytesDecoder)

meta = MetaData()
meta.reflect(bind=engine)
for table in meta.sorted_tables:
    Table = get_class_by_tablename(table.name)
    if not Table:
        continue
    for row in jsondata[table.name]:
        obj = Table(**row)
        session.add(obj)

session.commit()
