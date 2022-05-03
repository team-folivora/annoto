"""
Provides classes for Users
"""

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    """Basic information about a user"""

    username: str = Field(
        ..., description="The name of the user", example="team-folivora"
    )
    email: str = Field(
        ..., description="The email of the user", example="annoto@team-folivora.com"
    )


class CreateUserRequest(UserBase):
    """The fields required to create a new user"""

    password: str = Field(
        ..., description="The password of the user", example="test1234"
    )


class UserResponse(UserBase):
    """An already existing user"""

    id: int = Field(..., description="The id of the user", example=1)

    class Config:
        """Pydanic configuration"""

        orm_mode = True
