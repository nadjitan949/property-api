from pydantic import BaseModel, Field

class UserBase(BaseModel):
    firstname: str
    lastname: str
    email: str | None 
    phone: str | None

class UserAdd(UserBase):
    password: str


class ListUsersResponses(BaseModel):
    success: bool
    message: str
    data: list[UserBase]

class OneUserResponses(BaseModel):
    success: bool
    message: str
    data: UserBase
