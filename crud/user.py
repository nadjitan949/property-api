from sqlalchemy.orm import Session
from fastapi import HTTPException
from model.users import User
from schema.users import UserAdd, UserBase, UserUpdate
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
    

async def get_one_user(user_id: int, db: Session):
    try:
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            raise HTTPException(
                status_code=HTTP_STATUS_CODES["NOT_FOUND"],
                detail="Compte introuvable"
            )
        
        responses = {
            "success": True,
            "message": "Détails du compte",
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
    

async def create_user(data: UserAdd, db: Session):
    try:
    
        if data.id or data.created_at or data.updated_at:
            raise HTTPException(
                status_code=HTTP_STATUS_CODES["BAD_REQUEST"],
                detail="L'id, created_at et updated_at sont générés automatiquement et ne doivent pas être fournis. Veuillez les omettre ces champs lors de la création d'un compte."
            )

        if data.email:
            existEmail = db.query(User).filter(User.email == data.email).first()
            if existEmail:
                raise HTTPException(
                    status_code=HTTP_STATUS_CODES["CONFLICT"],
                    detail="Cet email est déjà associé à un autre compte"
                )
            
        if data.phone:
            existPhone = db.query(User).filter(User.phone == data.phone).first()
            if existPhone:
                raise HTTPException(
                    status_code=HTTP_STATUS_CODES["CONFLICT"],
                    detail="Ce numéro de téléphone appartient déjà à un autre compte"
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
    
    except HTTPException as http_err:
        raise http_err
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=HTTP_STATUS_CODES["INTERNAL_SERVER_ERROR"], 
            detail=f"Une erreur interne est survenue : {str(e)}"
        )
    
async def update_user(iuser_d: int, data: UserUpdate, db: Session):
    try:
        db_user = db.query(User).filter(User.id == iuser_d).first()
        if not db_user:
            raise HTTPException(
                status_code=HTTP_STATUS_CODES["NOT_FOUND"],
                detail="Utilisateur introuvable"
            )
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
        responses = {
            "success": True,
            "message": "Compte mis à jour !",
            "data": db_user
        }
        return responses
    
    except HTTPException as http_err:
        raise http_err
    
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_STATUS_CODES["INTERNAL_SERVER_ERROR"], 
            detail=f"Une erreur interne est survenue : {str(e)}"
        )

async def delete_user(user_id: int, db: Session):
    try:
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            raise HTTPException(
                status_code=HTTP_STATUS_CODES["NOT_FOUND"],
                detail="Utilisateur introuvable"
            )
        db.delete(db_user)
        db.commit()
        responses = {
            "success" : True,
            "message": "Compte supprimé",
            "data": db_user
        }

        return responses
    
    except HTTPException as http_err:
        raise http_err
    
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_STATUS_CODES["INTERNAL_SERVER_ERROR"],
            detail=f"Use erreur interne est survenu: {str(e)}"
        )
