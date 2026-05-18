import enum

from app.database.database import Base
from sqlalchemy import Column, String, Integer, Enum, func, DateTime

class OtpSource(enum.Enum):
    REGISTER = "register"
    FORGOT_PASSWORD = "forgot_password"

class Otp(Base):
    __tablename__ = "otps"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    source = Column(Enum(OtpSource), nullable=False)
    identity = Column(String, nullable=False, index=True)
    code = Column(String, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    def __repr__(self):
        return f"<Otp(identity={self.identity}, source={self.source}, code={self.code})>"