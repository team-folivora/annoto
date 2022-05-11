"""
Module for integration tests
"""

from bs4 import BeautifulSoup

from mod.src.settings import SETTINGS
from mod.tests.integration.conftest import ManagedTestClient


def assert_heading(page: BeautifulSoup, index: str) -> None:
    """Helper method to assert page heading"""
    assert page.body.find("h1").text == f"Index of {index}"


def assert_entry(page: BeautifulSoup, href: str, text: str) -> None:
    """Helper method to assert the page has a link to an entry"""
    assert page.body.find("a", attrs={"href": href}).text.strip() == text


def test_get_datafolder(client: ManagedTestClient) -> None:
    """Test GET /debug/data"""
    response = client.get(
        "/debug/data",
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    page = BeautifulSoup(response.text, features="html.parser")
    assert_heading(page, "/")
    assert_entry(page, "/debug/data/subfolder", "subfolder/")
    assert_entry(page, "/debug/data/sloth.jpg", "sloth.jpg")


def test_get_datafolder_sloth(client: ManagedTestClient) -> None:
    """Test GET /debug/data/sloth.jpg"""
    response = client.get(
        "/debug/data/sloth.jpg",
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/jpeg"


def test_get_datafolder_subfolder(client: ManagedTestClient) -> None:
    """Test GET /debug/data/subfolder"""
    response = client.get(
        "/debug/data/subfolder",
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    page = BeautifulSoup(response.text, features="html.parser")
    assert_heading(page, "/subfolder/")
    assert_entry(page, "/debug/data", "..")
    assert_entry(page, "/debug/data/subfolder/subsubfolder", "subsubfolder/")
    assert_entry(page, "/debug/data/subfolder/loremipsum.txt", "loremipsum.txt")


def test_get_datafolder_subfolder_loremipsum(client: ManagedTestClient) -> None:
    """Test GET /debug/data/subfolder/loremipsum.txt"""
    response = client.get(
        "/debug/data/subfolder/loremipsum.txt",
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/plain; charset=utf-8"


def test_get_datafolder_subfolder_subsubfolder(client: ManagedTestClient) -> None:
    """Test GET /debug/data/subfolder/subsubfolder"""
    response = client.get(
        "/debug/data/subfolder/subsubfolder",
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    page = BeautifulSoup(response.text, features="html.parser")
    assert_heading(page, "/subfolder/subsubfolder/")
    assert_entry(page, "/debug/data/subfolder", "..")


def test_get_datafolder_unknown_file_returns_404(client: ManagedTestClient) -> None:
    """Test GET /debug/data/unknown_file.txt"""
    response = client.delete(
        "/debug/data/unknown_file.txt",
    )
    assert response.status_code == 404


def test_delete_datafolder_file(client: ManagedTestClient) -> None:
    """Test DELETE /debug/data/sloth.jpg"""
    response = client.delete(
        "/debug/data/sloth.jpg",
    )
    assert response.status_code == 204
    assert not SETTINGS.data_folder.joinpath("sloth.jpg").exists()
    assert SETTINGS.data_folder.joinpath("subfolder").exists()


def test_delete_datafolder_directory(client: ManagedTestClient) -> None:
    """Test DELETE /debug/data/subfolder"""
    response = client.delete(
        "/debug/data/subfolder",
    )
    assert response.status_code == 204
    assert not SETTINGS.data_folder.joinpath("subfolder").exists()
    assert SETTINGS.data_folder.joinpath("sloth.jpg").exists()


def test_delete_datafolder_unknown_file_returns_404(client: ManagedTestClient) -> None:
    """Test DELETE /debug/data/unknown_file.txt"""
    response = client.delete(
        "/debug/data/unknown_file.txt",
    )
    assert response.status_code == 404


def test_delete_datafolder_root_fails(client: ManagedTestClient) -> None:
    """Test DELETE /debug/data/"""
    response = client.delete(
        "/debug/data/",
    )
    assert response.status_code == 400
