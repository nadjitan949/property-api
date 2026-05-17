from fastapi import Depends, status, APIRouter
from app.schema.properties import AllPropertyResponseModel, OnePropertyResponseModel, PropertyBase, UpdateProperty
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.crud.property import delete_property, get_all_properties, get_one_property, create_property, update_property

router = APIRouter(
    prefix="/properties",
    tags=["Annonces"]
)

@router.get("/all", response_model=AllPropertyResponseModel, status_code=status.HTTP_200_OK)
def all_property(db: Session = Depends(get_db)):
    return get_all_properties(db)

@router.get("/details/{property_id}", response_model=OnePropertyResponseModel, status_code=status.HTTP_200_OK)
def property_by_id(property_id: int, db: Session = Depends(get_db)):
    return get_one_property(property_id, db)

@router.post("/create", response_model=OnePropertyResponseModel, status_code=status.HTTP_201_CREATED)
def add_property(data: PropertyBase, db: Session = Depends(get_db)):
    return create_property(data, db)

@router.put("/update/{id}", response_model=OnePropertyResponseModel, status_code=status.HTTP_200_OK)
def property_update(id: int, data: UpdateProperty, db: Session = Depends(get_db)):
    return update_property(id, data, db)

@router.delete("/delete/{id}", response_model=OnePropertyResponseModel, status_code=status.HTTP_200_OK)
def property_delete(id: int, db: Session = Depends(get_db)):
    return delete_property(id, db)