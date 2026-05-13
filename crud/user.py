from sqlalchemy.orm import Session
from fastapi import HTTPException
from model.users import User
from schema.users import UserAdd
from messages.responses import HTTP_STATUS_CODES

async def get_all_users(db: Session):
    try:
        users = db.query(User).all()
        message = ""
        if len(users) == 0:
            message = "Aucun utilisateur enregisté pour le moment"
        else:
            message = "Liste des utilisateur"
        responses = {
            "success": True,
            "message": message,
            "data": users
        }
        return responses
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=HTTP_STATUS_CODES["INTERNAL_SERVER_ERROR"],
            detail=f"Une erreur interne est survenue : {str(e)}"
        )


async def create_user(data: UserAdd, db: Session):
    try:

        existEmail = db.query(User).filter(User.email == data.email).first()
        existPhone = db.query(User).filter(User.phone == data.phone).first()

        if existEmail:
            raise HTTPException(
                status_code=HTTP_STATUS_CODES["CONFLICT"],
                detail=("Cet email est déjà assosié à un autre compte")
            )
        
        if existPhone:
            raise HTTPException(
                status_code=HTTP_STATUS_CODES["CONFLICT"],
                detail=("Ce numéro de téléphone appartient déjà à un autre compte")
            )

        new_user = User(**data.model_dump())
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "success": True,
            "message": "Compte créé avec succès",
            "data": new_user
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=HTTP_STATUS_CODES["INTERNAL_SERVER_ERROR"], 
            detail=f"Une erreur interne est survenue : {str(e)}"
        )