"""Provides classes for login"""

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
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
        example="password",
    )


class LoginResponse(BaseModel):
    """
    Login token (JWT) and full user name
    """

    access_token: str = Field(
        ...,
        description="The generated JWT access token",
        example="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJleHBpcmVzIjoxNjUxNjcyMTU5LjMyMjY3ODZ9.ONVOoCKQ3ypaPgPAYCFnjlECzRdW9QgZsrkilnclnxg",  # pylint: disable=line-too-long
    )

    fullname: str = Field(
        ..., description="The fullname of the user", example="Prof. Dr. Folivora"
    )
