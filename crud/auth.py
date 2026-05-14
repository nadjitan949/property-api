from fastapi import HTTPException, responses
from sqlalchemy.orm import Session
from crud import user
from messages.responses import HTTP_STATUS_CODES
from model.users import User
from schema.auth import Login, Register
from passlib.context import CryptContext

psw_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__truncate_error=False)

async def login_user(data: Login, db: Session):
    try:
        if bool(data.email) == bool(data.phone):
            detail = "Fournissez soit un email, soit un téléphone." if not data.email else "Pas les deux en même temps."
            raise HTTPException(status_code=HTTP_STATUS_CODES["BAD_REQUEST"], detail=detail)
        
        if data.email:
            db_user = db.query(User).filter(User.email == data.email).first()
        else:
            db_user = db.query(User).filter(User.phone == data.phone).first()
            
        if not db_user or not psw_context.verify(data.password, db_user.password):
            raise HTTPException(
                status_code=HTTP_STATUS_CODES["UNAUTHORIZED"],
                detail="Email/Téléphone ou mot de passe incorrect"
            )
        
        responses = {
            "success": True,
            "message": "Connexion reussie",
            "data": db_user
        }

        return responses
        
    except HTTPException as http_err:
        raise http_err
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=HTTP_STATUS_CODES["INTERNAL_SERVER_ERROR"],
            detail=f"Une erreur interne est survenue : {str(e)}"
        )
    

async def register_user(data: Register, db: Session):
    try:

        if data.id or data.created_at or data.updated_at:
            raise HTTPException(
                status_code=HTTP_STATUS_CODES["BAD_REQUEST"],
                detail="Les champs id, created_at et updated_at sont gérés automatiquement et ne doivent pas être fournis."
            )

        if not data.email and not data.phone:
            raise HTTPException(
                status_code=HTTP_STATUS_CODES["BAD_REQUEST"],
                detail="Veuillez fournir soit un email, soit un numéro de téléphone pour vous inscrire."
            )
        if data.email:
            db_user = db.query(User).filter(User.email == data.email).first()
            if db_user:
                raise HTTPException(
                    status_code=HTTP_STATUS_CODES["CONFLICT"],
                    detail="Cet email est déjà associé à un autre compte"
                )
        if data.phone:
            db_user = db.query(User).filter(User.phone == data.phone).first()
            if db_user:
                raise HTTPException(
                    status_code=HTTP_STATUS_CODES["CONFLICT"],
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
            status_code=HTTP_STATUS_CODES["INTERNAL_SERVER_ERROR"],
            detail=f"Une erreur interne est survenue : {str(e)}"
        )
