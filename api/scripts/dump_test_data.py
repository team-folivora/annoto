import json
from pathlib import Path
from sqlalchemy import MetaData, create_engine
from mod.src.settings import SETTINGS


outfile_path = (
    Path.cwd().joinpath("mod").joinpath("fixtures").joinpath("test_data.json")
)


class BytesEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, bytes):
            return z.hex()
        return super().default(z)

engine = create_engine(SETTINGS.database_url, connect_args={"check_same_thread": False})
meta = MetaData()
meta.reflect(bind=engine)  # http://docs.sqlalchemy.org/en/rel_0_9/core/reflection.html
result = {}
for table in meta.sorted_tables:
    result[table.name] = [dict(row) for row in engine.execute(table.select())]
with open(outfile_path, "w") as f:
    f.write(json.dumps(result, cls=BytesEncoder, indent=4))
