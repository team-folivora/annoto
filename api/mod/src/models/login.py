"""Provides classes for login"""

from pydantic import BaseModel, Field


class LoginData(BaseModel):
    """
    The basic Login Data
    """

    username: str = Field(
        ...,
        description="The name of the user to be logged in",
        example="AnnotoUser#1337",
    )

    password: str = Field(
        ...,
        description="The password of the user to be logged in",
        example="test1234",
    )
