from pydantic import BaseModel

class OtpBase(BaseModel):
    email: str | None = None
    phone: str | None = None
    new_password: str | None = None
    
    code: str