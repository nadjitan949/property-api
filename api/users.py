from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database.database import get_db
from schema.users import UserAdd, OneUserResponses, ListUsersResponses
from crud.user import create_user, get_all_users
from model.users import User
from messages.responses import HTTP_STATUS_CODES

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get('/all', response_model=ListUsersResponses, status_code=HTTP_STATUS_CODES["OK"] )
async def read_all_users(db: Session = Depends(get_db)):
    return await get_all_users(db)

@router.post('/add', response_model=OneUserResponses, status_code=HTTP_STATUS_CODES["CREATED"])
async def add_user(data: UserAdd, db: Session = Depends(get_db)):
    return await create_user(data, db)