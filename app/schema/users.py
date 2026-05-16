from pydantic import BaseModel, ConfigDict
from datetime import datetime

class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int | None = None
    firstname: str
    lastname: str
    email: str | None = None
    phone: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

class UserAdd(UserBase):
    password: str

class UserUpdate(BaseModel):
    firstname: str | None = None
    lastname: str | None = None
    email: str | None = None
    phone: str | None = None


class ListUsersResponses(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    success: bool
    message: str
    data: list[UserBase]

class OneUserResponses(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    success: bool
    message: str
    data: UserBase | None = None
