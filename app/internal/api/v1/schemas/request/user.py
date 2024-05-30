from uuid import UUID

from pydantic import BaseModel

from internal.core.types import RolesEnum


class CreateRequest(BaseModel):
    username: str
    password: str
    role: RolesEnum = None


class GetDeleteRequest(BaseModel):
    user_id: UUID | None = None
    username: str | None = None
    role: RolesEnum | None = None


class UpdateRequest(BaseModel):
    user_id: UUID
    new_password: str | None = None
    new_role: str | None = None
