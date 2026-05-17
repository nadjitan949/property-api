from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.model.properties import PropertyType, TransactionType, PeriodeType
from app.model.users import UserRole

class PropertyFeatures(BaseModel):
    equipements: list[str] = []
    proximite: list[str] = []

class UserInProperty(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int | None = None
    firstname: str
    lastname: str
    email: str | None = None
    phone: str | None = None
    role: UserRole | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

class PropertyBase(BaseModel):
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
    features: PropertyFeatures | None = None
    owner_id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None
    owner: UserInProperty | None = None

class UpdateProperty(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str | None = None
    city: str | None = None
    address: str | None = None
    price: float | None = None
    periods: PeriodeType | None = None
    is_negotiable: bool | None = None
    description: str | None = None
    property_type: PropertyType | None = None
    transaction_type: TransactionType | None = None
    features: PropertyFeatures | None = None
    owner_id: int | None = None

class AllPropertyResponseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    success: bool
    message: str
    data: list[PropertyBase] | None = None

class OnePropertyResponseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    success: bool
    message: str
    data: PropertyBase | None = None