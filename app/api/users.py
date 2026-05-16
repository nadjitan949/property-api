from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schema.users import UserAdd, OneUserResponses, ListUsersResponses, UserUpdate
from app.crud.user import create_user, get_all_users, update_user, delete_user, get_one_user
from app.model.users import User
from app.core.dependencies.verify import get_cuurent_user

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get(
        '/all',
        response_model=ListUsersResponses,
        status_code=status.HTTP_200_OK,
        dependencies=[Depends(get_cuurent_user)]
        )
async def read_all_users(db: Session = Depends(get_db)):
    return await get_all_users(db)

@router.get('/details/{user_id}', response_model=OneUserResponses, status_code=status.HTTP_200_OK)
async def detail_user(user_id: int, db: Session = Depends(get_db)):
    return await get_one_user(user_id, db)

@router.post('/add', response_model=OneUserResponses, status_code=status.HTTP_201_CREATED)
async def add_user(data: UserAdd, db: Session = Depends(get_db)):
    return await create_user(data, db)

@router.put('/update/{user_id}', response_model=OneUserResponses, status_code=status.HTTP_200_OK)
async def user_update(user_id: int, data: UserUpdate, db: Session = Depends(get_db)):
    return await update_user(user_id, data, db)

@router.delete('/delete/{user_id}', response_model=OneUserResponses, status_code=status.HTTP_200_OK)
async def user_delete(user_id: int, db: Session = Depends(get_db)):
    return await delete_user(user_id, db)