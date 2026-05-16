from fastapi import APIRouter, Depends, status
from app.schema.auth import Login, AuthStatus, Register
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.crud.auth import login_user, register_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentification"]
)

@router.post("/sign-in", response_model=AuthStatus, status_code=status.HTTP_200_OK)
async def user_login(data: Login, db: Session = Depends(get_db)):
    return await login_user(data, db)

@router.post('/sign-up', response_model=AuthStatus, status_code=status.HTTP_200_OK)
async def user_register(data: Register, db: Session = Depends(get_db)):
    return await register_user(data, db)