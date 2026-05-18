from datetime import datetime
from typing import Optional
from app.model.users import UserRole

from pydantic import BaseModel, ConfigDict

class Login(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    email: str | None = None
    phone: str | None = None
    password: str


class Register(Login):
    model_config = ConfigDict(from_attributes=True)
    
    firstname: str
    lastname: str
    role: UserRole | None = None
    

class AuthResponses(Register):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class AuthStatus(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    success: bool
    message: str
    tokens: Optional[TokenSchema] = None
    data: AuthResponses
    