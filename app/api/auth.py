from fastapi import APIRouter, Depends, status
from app.model.users import User
from app.schema.auth import Login, AuthStatus, Register
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.crud.auth import login_user, register_user, me
from app.core.dependencies.verify import get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentification"]
)

@router.post("/sign-in", response_model=AuthStatus, status_code=status.HTTP_200_OK)
def user_login(data: Login, db: Session = Depends(get_db)):
    return login_user(data, db)

@router.post('/sign-up', response_model=AuthStatus, status_code=status.HTTP_200_OK)
def user_register(data: Register, db: Session = Depends(get_db)):
    return register_user(data, db)

@router.get("/me")
def my_account(current_user: User = Depends(get_current_user)):
    return me(current_user)