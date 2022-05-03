"""Provides classes for login"""

from pydantic import BaseModel, Field


class LoginData(BaseModel):
    """
    The basic Login Data
    """

    email: str = Field(
        ...,
        description="The email of the user to be logged in",
        example="team@folivora.online",
    )

    password: str = Field(
        ...,
        description="The password of the user to be logged in",
        example="test1234",
    )
