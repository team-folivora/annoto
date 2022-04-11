from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Dict

from pydantic import BaseModel

from mod.src.settings import SETTINGS


class AnnotationData(BaseModel):
    """
    The basic Annotation Data for a data file

    Attributes
        label           label the file [src] should be annotated with
        hash            hash of the file
        competency      the competencies the annotator has
        is_attentive    whether the annotator said that he is attentive
    """

    label: str
    hash: str
    competency: str
    is_attentive: bool


class Annotation(AnnotationData):
    """
    The Annotation of a data file

    Attributes
        src             name of the data file
    """

    src: str

    @classmethod
    def from_data(cls, annotation_data: AnnotationData, **kwargs: Dict) -> Annotation:
        """Creates an Annotation from AnnotationData and additional attributes"""
        return Annotation(**{**annotation_data.__dict__, **kwargs})

    @property
    def absolute_src(self) -> Path:
        """Returns the absolute path to the data file"""
        return SETTINGS.data_folder.joinpath(self.src)

    def file_exists(self) -> bool:
        """Returns whether the data file exists"""
        return self.absolute_src.is_file()

    def hash_is_valid(self) -> bool:
        """Returns the hash of the data file"""
        with open(self.absolute_src, "rb") as file:
            local_hash = hashlib.sha256(file.read()).hexdigest()
        return local_hash == self.hash

    def proofs_are_valid(self) -> bool:
        """Checks whether the proofs of the annotator are all valid"""
        return self.is_attentive and self.competency != ""

    def save(self) -> None:
        """
        Annotates the data file.
        Saves the result to the filesystem
        """
        if not self.file_exists():
            raise FileNotFoundError()
        if not self.proofs_are_valid():
            raise InvalidProof()
        if not self.hash_is_valid():
            raise HashMismatch()
        annotation_file = SETTINGS.data_folder.joinpath(f"{self.src}.annotation.json")
        with open(annotation_file, "w", encoding="utf-8") as file:
            file.write(json.dumps(self.__dict__, indent=4))


class HashMismatch(Exception):
    """Raised when the given hash of the annotation data doesn't match the generated hash of the data file"""

    pass


class InvalidProof(Exception):
    """Raised when proofs are invalid"""

    pass
