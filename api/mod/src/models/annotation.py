"""Provides classes for Annotations"""

import hashlib
import json
from pathlib import Path
from typing import Union

from pydantic import BaseModel, Field

from mod.src.settings import SETTINGS


class BaseAnnotationData(BaseModel):
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

    def proofs_are_valid(self) -> bool:
        """Checks whether the proofs of the annotator are all valid"""
        return self.is_attentive and self.competency != "" and self.is_trained


class ImageAnnotationData(BaseAnnotationData):
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


class FHIRECGAnnotationData(BaseAnnotationData):
    """
    The basic Annotation Data for a data file
    """


class ImageAnnotation(ImageAnnotationData):
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
    timestamp: int = Field(
        ...,
        description="The current timestamp when the annotation is saved",
        example=1652263830,
    )

    @classmethod
    def from_data(
        cls,
        annotation_data: ImageAnnotationData,
        src: str,
        fullname: str,
        timestamp: int,
    ) -> "ImageAnnotation":
        """Creates an Annotation from AnnotationData and additional attributes"""
        return ImageAnnotation(
            **{
                **annotation_data.__dict__,
                **{"src": src, "fullname": fullname, "timestamp": timestamp},
            }
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

    def save(self) -> None:
        """
        Annotates the data file.
        Saves the result to the filesystem
        """
        if not self.file_exists():
            raise FileNotFoundError()
        if not self.hash_is_valid():
            raise HashMismatch()
        annotation_file = SETTINGS.data_folder.joinpath(f"{self.src}.annotation.json")

        trial = 2
        while annotation_file.exists():
            annotation_file = SETTINGS.data_folder.joinpath(
                f"{self.src}.annotation.{trial}.json"
            )
            trial += 1

        with open(annotation_file, "w", encoding="utf-8") as file:
            file.write(json.dumps(self.__dict__, indent=4))


class HashMismatch(Exception):
    """
    Raised when the given hash of the annotation data
    doesn't match the generated hash of the data file
    """


class InvalidProof(Exception):
    """Raised when proofs are invalid"""


class FHIRECGAnnotation(FHIRECGAnnotationData):
    """
    The Annotation of a FHIR ECG
    """

    observationId: str = Field(
        ...,
        description="ID of the FHIR observation",
        example="285c6909-7ded-4dd8-92a7-a02501676ddb",
    )

    references: object = Field(
        ...,
        description="Reference to the generated annotated FHIR observations",
        example=[
            {"reference": "Observation/3c1b00db-41cd-4927-aa31-ffcd43e11677"},
            {"reference": "Observation/ac390dbe-6976-40e0-bfa8-4533dacb4647"},
        ],
    )

    @classmethod
    def from_data(
        cls,
        annotation_data: FHIRECGAnnotationData,
        observationId: str,
        references: object,
    ) -> "FHIRECGAnnotation":
        """Creates an Annotation from AnnotationData and additional attributes"""
        return FHIRECGAnnotation(
            **{
                **annotation_data.__dict__,
                **{"observationId": observationId, "references": references},
            }
        )

    def save(self) -> None:
        """
        Annotates the data file.
        Saves the result to the filesystem
        """
        annotation_file = SETTINGS.data_folder.joinpath(
            f"{self.observationId}.annotation.json"
        )

        trial = 2
        while annotation_file.exists():
            annotation_file = SETTINGS.data_folder.joinpath(
                f"{self.observationId}.annotation.{trial}.json"
            )
            trial += 1

        with open(annotation_file, "w", encoding="utf-8") as file:
            file.write(json.dumps(self.todict(), indent=4))

    def todict(self):  # FIXME
        d = self.__dict__
        del d["observationId"]
        return d


SpecificAnnotationData = Union[ImageAnnotationData, FHIRECGAnnotationData]
