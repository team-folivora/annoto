"""Provides classes for Annotations"""

import hashlib
import json
from pathlib import Path

from pydantic import BaseModel, Field

from mod.src.settings import SETTINGS


class AnnotationData(BaseModel):
    """
    The basic Annotation Data for a data file
    """

    label: str = Field(
        ..., description="The label the file should be annotated with", example="Sloth"
    )
    hash: str = Field(
        ...,
        description="The hash of the file",
        example="e922903b4d5431a8f9def3c89ffcb0b18472f3da304f28a2dbef9028b6cd205d",
    )
    competency: str = Field(
        ..., description="The competencies the annotator has", example="Prof. Dr. Med"
    )
    is_trained: bool = Field(
        ...,
        description="Whether the annotator said he finished the training",
        example=True,
    )
    is_attentive: bool = Field(
        ..., description="Whether the annotator said that he is attentive", example=True
    )


class Annotation(AnnotationData):
    """
    The Annotation of a data file
    """

    src: str = Field(
        ...,
        description="The location of the data file",
        example="ecg-qrs-classification-physiodb/sloth.jpg",
    )
    fullname: str = Field(
        ...,
        description="The full name of the annotator",
        example="Prof. Dr. Folivora",
    )

    @classmethod
    def from_data(
        cls, annotation_data: AnnotationData, src: str, fullname: str
    ) -> "Annotation":
        """Creates an Annotation from AnnotationData and additional attributes"""
        return Annotation(
            **{**annotation_data.__dict__, **{"src": src, "fullname": fullname}}
        )

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
        return self.is_attentive and self.competency != "" and self.is_trained

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
    """
    Raised when the given hash of the annotation data
    doesn't match the generated hash of the data file
    """


class InvalidProof(Exception):
    """Raised when proofs are invalid"""
