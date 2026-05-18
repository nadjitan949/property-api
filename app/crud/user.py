from sqlalchemy.orm import Session, selectinload
from fastapi import HTTPException, status
from app.model.users import User
from app.schema.users import UserAdd, UserUpdate, ResetUserPassword
from passlib.context import CryptContext

psw_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__truncate_error=False)

def get_all_users(db: Session):
    try:
        users = db.query(User).options(selectinload(User.properties)).all()
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
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Une erreur interne est survenue : {str(e)}"
        )
    

def get_one_user(user_id: int, db: Session):
    try:
        db_user = db.query(User).filter(User.id == user_id).options(selectinload(User.properties)).first()
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
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
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Une erreur interne est survenue : {str(e)}"
        )
    

def create_user(data: UserAdd, db: Session):
    try:

        if data.email:
            existEmail = db.query(User).filter(User.email == data.email).first()
            if existEmail:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Cet email est déjà associé à un autre compte"
                )
            
        if data.phone:
            existPhone = db.query(User).filter(User.phone == data.phone).first()
            if existPhone:
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
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Une erreur interne est survenue : {str(e)}"
        )
    
def update_user(user_id: int, data: UserUpdate, db: Session):
    try:
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
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
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Une erreur interne est survenue : {str(e)}"
        )

def delete_user(user_id: int, db: Session):
    try:
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
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
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Use erreur interne est survenu: {str(e)}"
        )

def reset_user_password(data: ResetUserPassword, db: Session):
    try:
        db_user = db.query(User).filter(User.id == data.user_id).first()
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Utilisateur introuvable"
            )
        hashedPassword = psw_context.hash(data.new_password)
        db_user.password = hashedPassword
        db.commit()
        db.refresh(db_user)
        responses = {
            "success": True,
            "message": "Mot de passe réinitialisé avec succès",
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