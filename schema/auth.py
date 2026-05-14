from datetime import datetime

from pydantic import BaseModel, ConfigDict

class Login(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    email: str | None = None
    phone: str | None = None
    password: str


class Register(Login):
    id: int | None = None
    firstname: str
    lastname: str
    created_at: datetime | None = None
    updated_at: datetime | None = None

class AuthStatus(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    success: bool
    message: str
    data: Register