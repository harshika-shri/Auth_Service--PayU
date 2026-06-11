from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr

from src.data.models.postgres.enums import UserRole


class CreateUserRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: UserRole


class UserResponse(BaseModel):
    id: UUID
    name: str
    email: str
    role: UserRole
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True,
    )


class UpdateUserStatusRequest(BaseModel):
    is_active: bool
