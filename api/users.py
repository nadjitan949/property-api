from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database.database import get_db
from schema.users import UserAdd, OneUserResponses, ListUsersResponses, UserUpdate
from crud.user import create_user, get_all_users, update_user, delete_user, get_one_user
from model.users import User
from messages.responses import HTTP_STATUS_CODES

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get('/all', response_model=ListUsersResponses, status_code=HTTP_STATUS_CODES["OK"] )
async def read_all_users(db: Session = Depends(get_db)):
    return await get_all_users(db)

@router.get('/details/{user_id}', response_model=OneUserResponses, status_code=HTTP_STATUS_CODES["OK"])
async def detail_user(user_id: int, db: Session = Depends(get_db)):
    return await get_one_user(user_id, db)

@router.post('/add', response_model=OneUserResponses, status_code=HTTP_STATUS_CODES["CREATED"])
async def add_user(data: UserAdd, db: Session = Depends(get_db)):
    return await create_user(data, db)

@router.put('/update/{user_id}', response_model=OneUserResponses, status_code=HTTP_STATUS_CODES["OK"])
async def user_update(user_id: int, data: UserUpdate, db: Session = Depends(get_db)):
    return await update_user(user_id, data, db)

@router.delete('/delete/{user_id}', response_model=OneUserResponses, status_code=HTTP_STATUS_CODES["OK"])
async def user_delete(user_id: int, db: Session = Depends(get_db)):
    return await delete_user(user_id, db)