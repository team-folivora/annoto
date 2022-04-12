"""Routes for debugging"""

import os
import shutil
from pathlib import Path, PurePath
from typing import Union

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from starlette.templating import _TemplateResponse

from mod.src.settings import SETTINGS

ROUTER = APIRouter(
    prefix="/debug",
    tags=["debug"],
)

TEMPLATE_DIRECTORY = Path.cwd().joinpath("mod").joinpath("src").joinpath("templates")
TEMPLATES = Jinja2Templates(TEMPLATE_DIRECTORY)


def path_url(path: PurePath) -> str:
    """Get the url to a path inside the data folder (~/.annoto)"""

    url_path = str(path.relative_to(SETTINGS.data_folder)).replace(os.path.sep, "/")
    return f"/debug/data/{url_path}" if url_path != "." else "/debug/data"


@ROUTER.get(
    "/data/{path:path}",
    response_class=FileResponse,
    responses={
        200: {
            "content": {
                "*": {"schema": {"type": "file", "format": "binary"}},
                "text/html": {},
            },
        },
        404: {"description": "File not found"},
    },
)
async def serve_data_folder(
    request: Request, path: str
) -> Union[FileResponse, _TemplateResponse]:
    """Serves the data folder (~/.annoto)"""

    path = SETTINGS.data_folder.joinpath(path)

    if path.is_file():
        return FileResponse(path)

    if path.is_dir():
        entries = list(
            map(
                lambda e: {
                    "name": f"{e}/" if path.joinpath(e).is_dir() else e,
                    "url": path_url(path.joinpath(e)),
                },
                os.listdir(path),
            )
        )

        base = f"{path_url(path)[len('/debug/data') :]}/"
        if base != "/":
            entries.insert(
                0,
                {
                    "name": "..",
                    "url": path_url(path.parent),
                },
            )

        return TEMPLATES.TemplateResponse(
            "list_directory.html",
            {
                "request": request,
                "entries": entries,
                "base": base,
            },
        )

    raise HTTPException(status_code=404, detail="File not found")


@ROUTER.delete(
    "/data/{path:path}",
    status_code=204,
    responses={
        404: {"description": "File not found"},
        400: {},
    },
)
async def delete_from_data_folder(path: str) -> None:
    """Delete from the data folder (~/.annoto)"""

    path = SETTINGS.data_folder.joinpath(path)
    if path == SETTINGS.data_folder:
        raise HTTPException(status_code=400)
    if path.is_file():
        os.remove(path)
    elif path.is_dir():
        shutil.rmtree(path)
    else:
        raise HTTPException(status_code=404, detail="File not found")
