from jose import jwt, ExpiredSignatureError, JWTError
from fastapi import HTTPException, status
from decouple import config
from datetime import datetime, timedelta, timezone



JWT_SECRET = config("JWT_SECRET")
ALGORITH = config("JWT_ALGORITHM")


def create_access_token(data: dict, expires_delta: int = 15):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITH)


def create_refresh_token(data: dict):
    expire = datetime.now(timezone.utc) + timedelta(days=7)
    to_encode = {"exp": expire, **data}
    return jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITH)


def verify_jwt_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITH])
        return payload

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )