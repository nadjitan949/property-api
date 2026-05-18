from datetime import datetime, timezone
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.model.otp import Otp, OtpSource
from app.model.users import User
from app.schema.otps import OtpBase
from passlib.context import CryptContext

psw_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__truncate_error=False)

def verify(data: OtpBase, db: Session):
    try:
        if bool(data.email) == bool(data.phone):
            detail = "Fournissez votre un email, soit votre téléphone."
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=detail
            )
        
        if data.email:
            db_otp = db.query(Otp).filter(Otp.identity == data.email).first()
            if not db_otp:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Aucun code OTP trouvé pour cet email"
                )
            
        elif data.phone:
            db_otp = db.query(Otp).filter(Otp.identity == data.phone).first()
            if not db_otp:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Aucun code OTP trouvé pour ce numéro de téléphone"
                )
            
        if not psw_context.verify(data.code, db_otp.code):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Code OTP invalide"
            )
        
        if db_otp.source == OtpSource.FORGOT_PASSWORD:
            if datetime.utcnow() > db_otp.expires_at:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Le code de réinitialisation a expiré (valide 1 min). Veuillez en demander un nouveau."
                )
        
            if data.email:
                db_user = db.query(User).filter(User.email == data.email).first()
            elif data.phone:
                db_user = db.query(User).filter(User.phone == data.phone).first()
            
            if not db_user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Aucun compte utilisateur trouvé pour cet email/numéro de téléphone"
                )
            
            hashedPassword = psw_context.hash(data.new_password)
            db_user.password = hashedPassword
            db.delete(db_otp)
            db.commit()
            db.refresh(db_user)


            responses = {
                "success": True,
                "message": "Code OTP vérifié avec succès",
                "data": db_user
            }
            return responses
        
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Une erreur interne est survenue : {str(e)}"
        )
        
