from fastapi import HTTPException, status, Depends, APIRouter
from app.database.database import get_db
from app.schema.otps import OtpBase
from app.schema.auth import AuthStatus
from sqlalchemy.orm import Session
from app.crud.otp import verify

router = APIRouter(
    prefix="/otp",
    tags=["Vérification OTP"]
)

@router.post("/verify", response_model=AuthStatus, status_code=status.HTTP_200_OK)
def otp_verify(data: OtpBase, db: Session = Depends(get_db)):
    return verify(data, db)

