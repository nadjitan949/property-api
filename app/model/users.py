import enum
from app.database.database import Base
from sqlalchemy import Column, DateTime, Integer, String, func, Enum
from sqlalchemy.orm import relationship

class UserRole(enum.Enum):
    USER = "user"
    AGENT = "agent"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False, index=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    email = Column(String, nullable=True, unique=True)
    phone = Column(String, nullable=True, unique=True)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.USER)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # properties = relationship("Property", back_populates="owner", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(username={self.firstname} {self.lastname}>"