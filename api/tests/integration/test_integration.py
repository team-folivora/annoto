import os
from flask import Response
import pytest
import shutil

from app import *

@pytest.fixture()
def app():
    app = create_app("config.TestingConfig")

    dst = app.config["DATA_FOLDER"]
    src = Path.cwd().joinpath("tests").joinpath("fixtures")
    shutil.copytree(src, dst, dirs_exist_ok=True)

    yield app

    shutil.rmtree(dst)


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_image(client):
    response:Response = client.get("/image")
    assert response.content_type == "image/jpg"
    assert response.status_code == 200
