"""
Module for integration tests
"""


import json
from pathlib import Path
import pytest
from pytest_mock import MockerFixture
import mod.src.app
from mod.src.app import Annotation
from pyfakefs.fake_filesystem_unittest import Patcher


@pytest.fixture
def annotation() -> Annotation:
    return Annotation(
        src="test.jpg",
        label="Label",
        hash="somehash",
        competency="Prof. Dr. Med.",
        is_attentive=True,
    )


class TestAnnotation:
    def test_absolute_src(self, annotation, mocker: MockerFixture) -> None:
        mocker.patch("mod.src.settings.SETTINGS.data_folder", Path("mock_folder"))
        assert Path("mock_folder/test.jpg") == annotation.absolute_src

    def test_file_exists(self, annotation) -> None:
        with Patcher(modules_to_reload=[mod.src.settings, mod.src.app]) as patcher:
            assert not annotation.file_exists()
            patcher.fs.create_file(
                mod.src.settings.SETTINGS.data_folder.joinpath("test.jpg")
            )
            assert annotation.file_exists()

    def test_raises_when_missing_src(self, annotation) -> None:
        """If src is not set, absolute_src should throw an error"""
        annotation.src = None
        with pytest.raises(AttributeError):
            annotation.absolute_src

    def test_hash_is_valid_returns_true_if_hash_is_valid(self, annotation) -> None:
        with Patcher(modules_to_reload=[mod.src.settings, mod.src.app]) as patcher:
            patcher.fs.create_file(
                mod.src.settings.SETTINGS.data_folder.joinpath("test.jpg"),
                contents="Dummy Content",
            )
            annotation.hash = (
                "a59ce92485a863931af21370b5082eb8a0c258c1cd74ae068db0ad47aeac1344"
            )
            assert annotation.hash_is_valid()

    def test_save_annotation_saves_annotation(self, annotation)->None:
        with Patcher(modules_to_reload=[mod.src.settings, mod.src.app]) as patcher:
            assert not mod.src.settings.SETTINGS.data_folder.joinpath("test.jpg.annotation.json").is_file()
            mod.src.settings.SETTINGS.data_folder.mkdir(exist_ok=True, parents=True)
            annotation.save()
            assert mod.src.settings.SETTINGS.data_folder.joinpath("test.jpg.annotation.json").is_file()
            with open(mod.src.settings.SETTINGS.data_folder.joinpath("test.jpg.annotation.json"), "r") as file:
                data = json.loads(file.read())
                assert data["src"] == "test.jpg"
                assert data["label"] == "Label"
