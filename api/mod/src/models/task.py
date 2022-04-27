"""Provides classes for Tasks"""

from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class Task(BaseModel):
    """
    A labelling task
    """

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
