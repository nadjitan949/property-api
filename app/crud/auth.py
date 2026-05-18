from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.model.users import User, UserRole
from app.model.otp import Otp, OtpSource
from app.schema.auth import Login, Register, UpdatePassword
from passlib.context import CryptContext
from app.core.tokens.generate import create_access_token, create_refresh_token
from app.core.secret.otp import generate_otp_code

psw_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__truncate_error=False)

def login_user(data: Login, db: Session):
    try:
        if bool(data.email) == bool(data.phone):
            detail = "Fournissez soit un email, soit un téléphone." if not data.email else "Pas les deux en même temps."
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=detail
                )
        
        if data.email:
            db_user = db.query(User).filter(User.email == data.email).first()
        else:
            db_user = db.query(User).filter(User.phone == data.phone).first()
            
        if not db_user or not psw_context.verify(data.password, db_user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email/Téléphone ou mot de passe incorrect"
            )
        
        access_token = create_access_token(data={"sub": str(db_user.id)})
        refresh_token = create_refresh_token(data={"sub": str(db_user.id)})
        
        responses = {
            "success": True,
            "message": "Connexion reussie",
            "tokens": {
                "access_token": access_token,
                "refresh_token": refresh_token
            },
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
    

def register_user(data: Register, db: Session):
    try:

        if data.role and data.role == UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Vous n'avez pas les permissions nécessaires pour créer un compte administrateur."
            )

        if not data.email and not data.phone:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Veuillez fournir soit un email, soit un numéro de téléphone pour vous inscrire."
            )
        if data.email:
            db_user = db.query(User).filter(User.email == data.email).first()
            if db_user:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Cet email est déjà associé à un autre compte"
                )
        if data.phone:
            db_user = db.query(User).filter(User.phone == data.phone).first()
            if db_user:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Ce numéro de téléphone appartient déjà à un autre compte"
                )
            
        user_data = data.model_dump()
        user_data.pop('password')
        hashed_password = psw_context.hash(data.password)
            
        new_user = User(
            password = hashed_password,
            **user_data
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        responses = {
            "success": True,
            "message": "Compte créé avec succès",
            "data": new_user
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
    

def me(current_user: User):
    try:
        responses = {
            "success": True,
            "message": "Profil récupéré avec succès",
            "data": current_user
        }
        return responses
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Une erreur est survenue lors de la récupération du profil : {str(e)}"
        )
    
def reset_password(current_user: int, data: UpdatePassword, db: Session):
    try:
        db_user = db.query(User).filter(User.id == current_user)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Veuillez vous connecter pour réinitialiser votre mot de passe"
            )
        
        if data.old_password and not psw_context.verify(data.old_password, db_user.first().password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Ancien mot de passe incorrect"
            )
        new_hashed_password = psw_context.hash(data.new_password)
        db_user.update({"password": new_hashed_password})
        db.commit()
        db.refresh(db_user.first())
        responses = {
            "success": True,
            "message": "Mot de passe réinitialisé avec succès",
            "data": db_user.first()
        }
        return responses
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Une erreur est survenue lors de la réinitialisation du mot de passe : {str(e)}"
        )

def forgot_password(data: UpdatePassword, db: Session):
    try:
        if bool(data.email) == bool(data.phone):
            detail = "Fournissez soit votre email, soit votre téléphone."
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=detail
                )
        
        identity = None
        message = ""
        expiration = 1

        if data.email:
            identity = data.email
            db_user = db.query(User).filter(User.email == data.email).first()
            if not db_user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Votre adresse email n'est associée à aucun compte"
                )
            identity = db_user.email
            message = f"Un code de réinitialisation a été envoyé à l'adresse {data.email}"
        elif data.phone:
            identity = data.phone
            db_user = db.query(User).filter(User.phone == data.phone).first()
            if not db_user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Votre numéro de téléphone n'est associé à aucun compte"
                )
            identity = db_user.phone
            message = f"Un code de réinitialisation a été envoyé au numéro {data.phone} expire dans {expiration} min"

        db.query(Otp).filter(
            Otp.identity.in_([db_user.email, db_user.phone]),
            Otp.source == OtpSource.FORGOT_PASSWORD
        ).delete(synchronize_session=False)
            
        otpCode = generate_otp_code()
        hashedOtp = psw_context.hash(otpCode)

        time_to_expire = datetime.now(timezone.utc) + timedelta(minutes=expiration)

        new_otp = Otp(
            source = OtpSource.FORGOT_PASSWORD,
            code = hashedOtp,
            identity = identity,
            expires_at = time_to_expire
        )

        db.add(new_otp)
        db.commit()
        db.refresh(new_otp)
            
        responses = {
            "success": True,
            "message": message,
            "data": otpCode
        }
        return responses

    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Une erreur est survenue lors de la réinitialisation du mot de passe : {str(e)}"
        )
        

