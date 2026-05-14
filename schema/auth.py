from pydantic import BaseModel, ConfigDict

class Login(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    email: str | None = None
    phone: str | None = None
    password: str


class Register(Login):
    firstname: str
    lastname: str

class AuthStatus(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    success: bool
    message: str
    data: Register