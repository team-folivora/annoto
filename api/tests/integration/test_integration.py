from flask import Response
import pytest

from app import *

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app

    # clean up / reset resources here


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
