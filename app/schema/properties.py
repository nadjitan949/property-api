from pydantic import BaseModel, ConfigDict
from app.model.properties import PropertyType, PropertyStatus, TransactionType

class PropertyBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    title: str
    city: str
    address: str
    description: str | None = None
    property_type: PropertyType
    transaction_type: TransactionType
    features: dict
    owner_id: int

class UpdateProperty(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str | None = None
    city: str | None = None
    address: str | None = None
    description: str | None = None
    property_type: PropertyType | None = None
    transaction_type: TransactionType | None = None
    features: dict | None = None
    owner_id: int | None = None

class ResponseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    success: bool
    message: str
    data: PropertyBase | None = None