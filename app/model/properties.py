import enum

from app.database.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Enum, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

class PropertyType(enum.Enum):
    STUDIO = "studio"
    APARTMENT = "apartment"
    HOUSE = "house"
    TERRAIN = "terrain"
    COMMERCIAL = "commercial"

class TransactionType(enum.Enum):
    RENT = "rent"
    SALE = "sale"

class PropertyStatus(enum.Enum):
    AVAILABLE = "available"
    PENDING = "pending"
    ARCHIVED = "archived"


class Property(Base):
    __tablename__ = "properties"
    
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False, index=True)
    title = Column(String, nullable=False)
    city = Column(String, nullable=False)
    address = Column(String, nullable=False)
    property_type = Column(Enum(PropertyType), nullable=False)
    Transaction_type = Column(Enum(TransactionType), nullable=False)
    Property_status = Column(Enum(PropertyStatus), nullable=False, default=PropertyStatus.AVAILABLE)
    features = Column(JSONB, nullable=True, default=dict)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User", back_populates="properties")

    def __repr__(self):
        return f"<Property(title={self.title}, type={self.property_type})>"