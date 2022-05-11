import json

from mod.src.database import database, db_models
from scripts.config import file_path, meta, session
from typing import Optional, Any, Callable, Tuple, List


def get_class_by_tablename(tablename: str) -> Optional[type]:
    base = database.Base

    for mapper in base.registry.mappers:
        if mapper.class_.__tablename__ == tablename:
            return mapper.class_
    return None


class BytesDecoder(json.JSONDecoder):
    def __init__(
        self,
        *args: Any,
        **kwargs: Any,
    ):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, dct: dict) -> dict:
        """ "Byte data is recognised from the JSON file and directly decoded as bytes-object"""
        for key in dct.keys():
            if isinstance(dct[key], str) and dct[key].startswith("0x"):
                dct[key] = bytes.fromhex(dct[key][2:])
        return dct


def load() -> None:
    """Loads all objects from 'test_data.json' into the database that have a corresponding defined model class"""
    with open(file_path) as f:
        data = f.read()
        jsondata = json.loads(data, cls=BytesDecoder)

    for table in meta.sorted_tables:
        if table.name != "alembic_version":
            Table = get_class_by_tablename(table.name)
            for row in jsondata[table.name]:
                if not Table:
                    print(f"Warning: Alembic Model for table {table.name} not found")
                    continue
                obj = Table(**row)
                session.add(obj)

    session.commit()


if __name__ == "__main__":
    load()
