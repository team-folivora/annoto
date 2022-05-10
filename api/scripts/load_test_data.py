import json

from mod.src.database import database, db_models
from scripts.config import file_path, meta, session


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
    """Loads all objects from 'test_data.json' into the database that have a corresponding defined model class"""
    with open(file_path) as f:
        data = f.read()
        jsondata = json.loads(data, cls=BytesDecoder)

    for table in meta.sorted_tables:
        if table.name != "alembic_version":
            Table = get_class_by_tablename(table.name)
            for row in jsondata[table.name]:
                obj = Table(**row)
                session.add(obj)

    session.commit()


if __name__ == "__main__":
    load()
