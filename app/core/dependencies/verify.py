import os
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.model.users import User
from dotenv import load_dotenv
import jwt

load_dotenv()

SECRET_KEY = os.getenv("SECRET_TOKEN")
ALGORITHM = os.getenv("ALGORITHM_TOKEN", "HS256")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/sign-in")

async def get_cuurent_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalide ou expiré",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get("type") != "access":
            raise credentials_exception
        
        user_id: str = payload.get("sub")

        if user_id is None:
            raise credentials_exception
        
    except jwt.PyJWKError:
        raise credentials_exception
    
    db_user = db.query(User).filter(User.id == user_id).first()

    if db_user is None:
        raise credentials_exception
    
    return db_user