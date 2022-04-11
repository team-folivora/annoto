"""
Module for integration tests
"""


import json
from pathlib import Path

import pytest
from pytest_mock import MockerFixture

import mod.src.app
from mod.src.models.annotation import Annotation
from mod.src.settings import SETTINGS


@pytest.fixture
def annotation() -> Annotation:
    """Creates a basic Annotation"""
    return Annotation(
        src="test.jpg",
        label="Label",
        hash="a59ce92485a863931af21370b5082eb8a0c258c1cd74ae068db0ad47aeac1344",
        competency="Prof. Dr. Med.",
        is_attentive=True,
    )


class TestAnnotation:
    """Tests the Annotation"""

    def test_absolute_src(self, annotation: Annotation, mocker: MockerFixture) -> None:
        """Tests if the path to the data file is correctly generated"""
        mocker.patch("mod.src.settings.SETTINGS.data_folder", Path("mock_folder"))
        assert Path("mock_folder/test.jpg") == annotation.absolute_src

    def test_file_exists(self, annotation: Annotation) -> None:
        """Tests if the file exists"""
        assert not annotation.file_exists()
        with open(annotation.absolute_src, "w", encoding="utf-8") as file:
            file.write("Test File")
        assert annotation.file_exists()

    def test_hash_is_valid_returns_true_if_hash_is_valid(
        self, annotation: Annotation
    ) -> None:
        """Tests if the hash-test function returns True
        if the hash provided with the AnnotationData is valid"""
        with open(annotation.absolute_src, "w", encoding="utf-8") as file:
            file.write("Dummy Content")
        annotation.hash = (
            "a59ce92485a863931af21370b5082eb8a0c258c1cd74ae068db0ad47aeac1344"
        )
        assert annotation.hash_is_valid()

    def test_save_annotation_saves_annotation(self, annotation: Annotation) -> None:
        """Tests whether the Annotation is correctly saved"""
        assert not SETTINGS.data_folder.joinpath("test.jpg.annotation.json").is_file()
        with open(annotation.absolute_src, "w", encoding="utf-8") as file:
            file.write("Dummy Content")
        annotation.save()
        assert SETTINGS.data_folder.joinpath("test.jpg.annotation.json").is_file()
        with open(
            mod.src.settings.SETTINGS.data_folder.joinpath("test.jpg.annotation.json"),
            "r", encoding="utf-8"
        ) as file:
            data = json.loads(file.read())
            assert data == annotation.__dict__
