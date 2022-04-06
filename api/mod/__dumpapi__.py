from fastapi.openapi.utils import get_openapi

from mod.src.app import APP

openapi_schema = get_openapi(
    title="Annoto API",
    version="v1",
    routes=APP.routes,
)
print(openapi_schema)
