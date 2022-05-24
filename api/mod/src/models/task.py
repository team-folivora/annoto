"""Provides classes for Tasks"""

import json
from pathlib import Path
from typing import List, Union

from pydantic import BaseModel, Field
from enum import Enum


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


class FHIRECGTask(BaseTask):
    pass


task_types = {
    TaskType.IMAGE_CLASSIFICATION: ImageTask,
    TaskType.FHIR_ECG_ANNOTATION: FHIRECGTask,
}

SpecificTask = Union[ImageTask, FHIRECGTask]


class TaskNotFoundException(Exception):
    pass
