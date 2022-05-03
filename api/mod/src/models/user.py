"""
Provides classes for Users
"""

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    """Basic information about a user"""

    fullname: str = Field(
        ..., description="The full name of the user", example="Prof. Dr. Folivora"
    )
    email: str = Field(
        ..., description="The email of the user", example="team@folivora.online"
    )


class CreateUserRequest(UserBase):
    """The fields required to create a new user"""

    password: str = Field(
        ..., description="The password of the user", example="password"
    )


class UserResponse(UserBase):
    """An already existing user"""

    id: int = Field(..., description="The id of the user", example=1)

    class Config:
        """Pydanic configuration"""

        orm_mode = True
