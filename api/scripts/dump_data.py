import json
from pathlib import Path

from mod.src.settings import SETTINGS
from scripts import engine, file_path, meta


class BytesEncoder(json.JSONEncoder):
    """Byte data is encoded as a hexadecimal string and prefixed with 0x to be recognised during decoding"""

    def default(self, z):
        if isinstance(z, bytes):
            return "0x" + z.hex()
        return super().default(z)


def dump():
    """Dumps all entries from the database into 'test_data.json'"""
    result = {}
    for table in meta.sorted_tables:
        if table.name != "alembic_version":
            result[table.name] = [dict(row) for row in engine.execute(table.select())]
    with open(file_path, "w") as f:
        f.write(json.dumps(result, cls=BytesEncoder, indent=4))
