import json
from pathlib import Path

from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker

from mod.src.database import database, db_models
from mod.src.settings import SETTINGS


def get_class_by_tablename(tablename):
    base = database.Base

    for mapper in base.registry.mappers:
        if mapper.class_.__tablename__ == tablename:
            return mapper.class_


class BytesDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, dct):
        """ "Byte data is recognised from the JSON file and directly decoded as bytes-object"""
        for key in dct.keys():
            if isinstance(dct[key], str) and dct[key].startswith("0x"):
                dct[key] = bytes.fromhex(dct[key][2:])
        return dct

def load():
    file_path = Path.cwd().joinpath("mod").joinpath("fixtures").joinpath("test_data.json")

    if not file_path.exists():
        print("File does not exist")
        exit(1)

    engine = create_engine(SETTINGS.database_url, connect_args={"check_same_thread": False})

    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    with open(file_path) as f:
        data = f.read()
        jsondata = json.loads(data, cls=BytesDecoder)

    meta = MetaData()
    meta.reflect(bind=engine)
    for table in meta.sorted_tables:
        Table = get_class_by_tablename(table.name)
        if not Table:
            print(f"DB Model Class not found for table: {table.name}")
            continue
        for row in jsondata[table.name]:
            obj = Table(**row)
            session.add(obj)

    session.commit()
