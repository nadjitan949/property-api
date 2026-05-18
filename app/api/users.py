from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schema.users import ResetUserPassword, UserAdd, OneUserResponses, ListUsersResponses, UserUpdate
from app.crud.user import create_user, get_all_users, reset_user_password, update_user, delete_user, get_one_user
from app.model.users import User
from app.core.dependencies.verify import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get(
        '/all',
        response_model=ListUsersResponses,
        status_code=status.HTTP_200_OK,
        dependencies=[Depends(get_current_user)]
        )
def read_all_users(db: Session = Depends(get_db)):
    return get_all_users(db)

@router.get('/details/{user_id}', response_model=OneUserResponses, status_code=status.HTTP_200_OK)
def detail_user(user_id: int, db: Session = Depends(get_db)):
    return get_one_user(user_id, db)

@router.post('/add', response_model=OneUserResponses, status_code=status.HTTP_201_CREATED)
def add_user(data: UserAdd, db: Session = Depends(get_db)):
    return create_user(data, db)

@router.put('/update/{user_id}', response_model=OneUserResponses, status_code=status.HTTP_200_OK)
def user_update(user_id: int, data: UserUpdate, db: Session = Depends(get_db)):
    return update_user(user_id, data, db)

@router.delete('/delete/{user_id}', response_model=OneUserResponses, status_code=status.HTTP_200_OK)
def user_delete(user_id: int, db: Session = Depends(get_db)):
    return delete_user(user_id, db)

@router.patch('/reset-user-password', response_model=OneUserResponses, status_code=status.HTTP_200_OK)
def user_password_reset(data: ResetUserPassword, db: Session = Depends(get_db)):
    return reset_user_password(data, db)