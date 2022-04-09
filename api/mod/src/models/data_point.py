import hashlib
import json
from pathlib import Path

from pydantic import BaseModel

from mod.src.settings import SETTINGS


class Annotation(BaseModel):
    """
    An annotation of a file

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

    def proofs_are_valid(self) -> bool:
        """Checks whether the proofs of the annotator are all valid"""
        return self.is_attentive


class DataPoint(BaseModel):
    src: str

    @property
    def absolute_src(self) -> Path:
        """Returns the absolute path to the data file"""
        return SETTINGS.data_folder.joinpath(self.src)

    def file_exists(self) -> bool:
        """Returns whether the data file exists"""
        return self.absolute_src.is_file()

    def hash(self) -> str:
        """Returns the hash of the data point"""
        with open(self.absolute_src, "rb") as file:
            local_hash = hashlib.sha256(file.read()).hexdigest()
        return local_hash

    def annotate(self, annotation: Annotation) -> None:
        """
        Annotates this data point with the given annotation.
        Saves the result to the filesystem
        """
        if self.hash != annotation.hash:
            raise HashMismatch("Hash mismatch")
        annotation_file = SETTINGS.data_folder.joinpath(f"{self.src}.annotation.json")
        with open(annotation_file, "w", encoding="utf-8") as file:
            file.write(json.dumps(annotation.__dict__, indent=4))


class HashMismatch(Exception):
    """Raised when the hash of the data point does not match the hash of the annotation"""

    pass
