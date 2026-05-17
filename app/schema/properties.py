from pydantic import BaseModel, ConfigDict
from app.model.properties import PropertyType, TransactionType, PeriodeType

class PropertyFeatures(BaseModel):
    equipements: list[str] = []
    proximite: list[str] = []

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

class ResponseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    success: bool
    message: str
    data: PropertyBase | None = None