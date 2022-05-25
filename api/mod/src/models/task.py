"""Provides classes for Tasks"""

import json
import os
import random
import re
import time
from abc import abstractmethod
from enum import Enum
from pathlib import Path
from typing import List, Union

from pydantic import BaseModel, Field

from mod.src.auth.auth_bearer import JWTBearer
from mod.src.auth.auth_handler import JWTPayload
from mod.src.models.annotation import (
    BaseAnnotationData,
    FHIRECGAnnotationData,
    ImageAnnotation,
    ImageAnnotationData,
)
from mod.src.settings import SETTINGS


class TaskType(Enum):
    UNKNOWN = "unknown"
    IMAGE_CLASSIFICATION = "image_classification"
    FHIR_ECG_ANNOTATION = "fhir_ecg_annotation"


class BaseTask(BaseModel):
    """
    A labeling task
    """

    type_id: TaskType = Field(
        ...,
        description="The type of the task",
        example=TaskType.FHIR_ECG_ANNOTATION,
    )

    id: str = Field(
        ...,
        description="The identifier of this labelling task",
        example="ecg-qrs-classification-physiodb",
    )

    description: str = Field(
        ...,
        description="A brief description of this labelling task",
        example="Classifying the QRS complex of some ECGs",
    )

    @classmethod
    def from_dict(cls, data: dict) -> "SpecificTask":
        """
        Creates a task from a type id
        """
        return task_types[TaskType(data["type_id"])](**data)

    @classmethod
    def load_from_file(cls, path: Path) -> "SpecificTask":
        """
        Loads a task from a file
        """
        if not path.exists():
            raise Exception("Task file not found")
        with open(path, "r", encoding="utf-8") as file:
            return cls.from_dict(json.load(file))

    def next_sample(self):
        raise NotImplementedError

    def save_annotation(
        self, sample_id: str, annotation_data: BaseAnnotationData, jwt: JWTPayload
    ):
        raise NotImplementedError


class ImageTask(BaseTask):
    labels: List[str] = Field(
        ...,
        description="List of labels",
        example=[
            "Atrial fibrillation",
            "Normal sinus rhythm",
            "Ventricular tachycardia",
            "Noise",
            "Other",
        ],
    )

    def next_sample(self) -> Union[str, None]:
        task_folder = SETTINGS.data_folder.joinpath(self.id)
        images = list(
            filter(
                lambda f: re.match(".*\\.(png|jpg|jpeg)$", f), os.listdir(task_folder)
            )
        )
        images = list(
            filter(
                lambda f: not task_folder.joinpath(f"{f}.annotation.json").exists(),
                images,
            )
        )
        return random.choice(images) if images else None

    def save_annotation(
        self, sample_id: str, annotation_data: ImageAnnotationData, jwt: JWTPayload
    ):
        annotation = ImageAnnotation.from_data(
            annotation_data=annotation_data,
            src=f"{self.id}/{sample_id}",
            fullname=jwt.fullname,
            timestamp=int(time.time()),
        )
        annotation.save()


class FHIRECGTask(BaseTask):
    def next_sample(self):
        return "da576f2e-7529-4790-8991-c8300a16ae67"

    def save_annotation(
        self, sample_id: str, annotation_data: FHIRECGAnnotationData, jwt: JWTPayload
    ):
        pass


task_types = {
    TaskType.IMAGE_CLASSIFICATION: ImageTask,
    TaskType.FHIR_ECG_ANNOTATION: FHIRECGTask,
}

SpecificTask = Union[ImageTask, FHIRECGTask]


class TaskNotFoundException(Exception):
    pass
