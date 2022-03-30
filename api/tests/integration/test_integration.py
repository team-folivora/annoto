'''
Module for integration tests
'''

from pathlib import Path
import shutil
import tempfile
import pytest
from fastapi.testclient import TestClient

from api.src.settings import SETTINGS
from api.src.app import APP


def pytest_sessionstart() -> None:
    '''Setup testing session'''
    SETTINGS.data_loader = Path(tempfile.mkdtemp(prefix="annoto"))
    SETTINGS.testing = True

    dst = SETTINGS.data_loader
    src = Path.cwd().joinpath("tests").joinpath("fixtures")
    shutil.copytree(src, dst, dirs_exist_ok=True)


def pytest_sessionend() -> None:
    '''Teardown testing session'''
    shutil.rmtree(SETTINGS.data_loader)


@pytest.fixture()
def client() -> TestClient:
    '''Get a client for testing the api'''
    return TestClient(APP)


def test_image(client: TestClient) -> None:
    '''Test GET /image'''
    response = client.get("/image")
    assert response.status_code == 200
    assert response.headers['content-type'] == "image/jpeg"
