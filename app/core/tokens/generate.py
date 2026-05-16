import os
import jwt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

SECRETE_KEY = os.getenv("SECRET_TOKEN")
ALGORITHM = os.getenv("ALGORITHM_TOKEN", "HS256")

ACCESS_TOKEN_EXPIRE = int(os.getenv("EXPIRE_ACCESS_TOKEN"))
REFRES_TOKEN_EXPIRE = int(os.getenv("EXPIRE_REFRESH_TOKEN"))

def create_access_token(data: dict, expire_delta: Optional[timedelta] = None) -> str:

    to_encode = data.copy()
    if expire_delta:
        expire = datetime.now(timezone.utc) + expire_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE)

    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, SECRETE_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict, expire_delta: Optional[timedelta] = None):

    to_encode = data.copy()
    if expire_delta:
        expire = datetime.now(timezone.utc) + expire_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=REFRES_TOKEN_EXPIRE)

    to_encode.update({"exp": expire, "type": "refresh"})

    return jwt.encode(to_encode, SECRETE_KEY, algorithm=ALGORITHM)

