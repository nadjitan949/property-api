from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.model.users import UserRole
from app.model.properties import PeriodeType, TransactionType, PropertyType

class PropertyFeatures(BaseModel):
    equipements: list[str] = []
    proximite: list[str] = []

class PropertiesInUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    title: str
    city: str
    address: str
    price: float
    periods: PeriodeType | None = None
    is_negotiable: bool
    description: str | None = None
    property_type: PropertyType
    transaction_type: TransactionType
    owner_id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None
    features: PropertyFeatures | None = None

class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    firstname: str
    lastname: str
    email: str | None = None
    phone: str | None = None
    role: UserRole | None = None

class UserAdd(UserBase):
    password: str

class UserUpdate(BaseModel):
    firstname: str | None = None
    lastname: str | None = None
    email: str | None = None
    phone: str | None = None
    role: UserRole | None = None

class UserResponses(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    properties: list[PropertiesInUser] | None = None


class ListUsersResponses(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    success: bool
    message: str
    data: list[UserResponses]

class OneUserResponses(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    success: bool
    message: str
    data: UserResponses | None = None
