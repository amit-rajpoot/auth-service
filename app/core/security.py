#Security Functions
from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, status
from jose import jwt, JWTError
from app.core.config import ALGORITHM, SECRET_KEY, pwd_context
from app.schemas.auth import TokenData


def verify_pwd(plain_pwd: str, hashed_pwd: str) -> bool:
    return pwd_context.verify(plain_pwd, hashed_pwd)


def get_pwd_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


def verify_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email: str = payload.get("sub")

        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not Verify Credentials",
                headers={"WWW-Authenticate": "Bearer"}
            )

        return TokenData(email=email)

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not Verify Credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )