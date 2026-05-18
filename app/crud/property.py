from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload
from app.model.properties import Property
from app.model.users import User
from app.schema.properties import PropertyBase, UpdateProperty

def get_all_properties(db: Session):
    try:
        db_properties = db.query(Property).options(joinedload(Property.owner)).all()
        if len(db_properties) == 0:
            message = "Aucun annonce immobilière enregisté pour le moment"
        else:
            message = "Liste des annonces immobilières"

        responses = {
            "success": True,
            "message": message,
            "data": db_properties
        }

        return responses

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des propriétés {str(e)}"
        )
    
def get_one_property(property_id: int, db: Session):
    try:
        db_property = db.query(Property).filter(Property.id == property_id).options(joinedload(Property.owner)).first()
        if not db_property:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Propriété introuvable"
            )
        
        responses = {
            "success": True,
            "message": "Détails de la propriété",
            "data": db_property
        }

        return responses
    
    except HTTPException as http_err:
        raise http_err
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération de la propriété {str(e)}"
        )
def create_property(data: PropertyBase, db: Session):
    try:
        
        db_owner = db.query(User).filter(User.id == data.owner_id).first()
        if not db_owner:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Propriétaire introuvable"
            )
        property_data = Property(**data.model_dump())
        db.add(property_data)
        db.commit()
        db.refresh(property_data)

        responses = {
            "success": True,
            "message": "Propriété créée avec succès",
            "data": property_data
        }

        return responses
    
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la création de la propriété {str(e)}"
        )
    

def update_property(id: int, data: UpdateProperty, db: Session):
    try:
        db_property = db.query(Property).filter(Property.id == id)
        if not db_property:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Propriété introuvable"
            )
        update_data = data.model_dump(exclude_unset=True)
        if 'owner_id' in update_data:
            db_owner = db.query(User).filter(User.id == update_data['owner_id']).first()
            if not db_owner:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Propriétaire introuvable"
                )
        db_property.update(update_data)
        db.commit()
        db.refresh(db_property.first())
        responses = {
            "success": True,
            "message": "Propriété mise à jour avec succès",
            "data": db_property.first()
        }
        return responses
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la mise à jour de la propriété {str(e)}"
        )

def delete_property(id: int, db: Session):
    try:
        db_property = db.query(Property).filter(Property.id == id).first()
        if not db_property:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Propriété introuvable"
            )
        db.delete(db_property)
        db.commit()
        responses = {
            "success": True,
            "message": "Propriété supprimée avec succès",
            "data": db_property
        }
        return responses
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la suppression de la propriété {str(e)}"
        )