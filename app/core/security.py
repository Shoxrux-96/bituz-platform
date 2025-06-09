from typing import Annotated
from jose import JWTError, jwt
from utils.hashing import pwd_context
from decouple import config

from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

from core.database import get_db
from models.user import User, Role
from sqlalchemy.orm import Session


# Password utilities
JWT_SECRET = config("JWT_SECRET")
ALGORITH = config("JWT_ALGORITHM")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


def authenticate_user(email: str, password: str, db):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return False
    if not pwd_context.verify(password, user.password):
        return False
    return user


def get_user(email,db : Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    return user


def is_user(token: Annotated[str, Depends(oauth2_scheme)], db : Session = Depends(get_db)):
    """ User permission"""
    try:
        payload  = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITH])
        email = payload.get("sub")
        user_id = payload.get("id")
        if email is None or user_id is None:
             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Foydalanuvchi topilmadi")
        user = get_user(email, db)
        return user
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Qayta Login qilib ko'ring token xatolik")
    
    
def is_super_user(token: Annotated[str, Depends(oauth2_scheme)], db : Session = Depends(get_db)):
    """ Super user permission """
    try:
        payload  = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITH])
        email = payload.get("sub")
        user_id = payload.get("id")
        if email is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Foydalanuvchi topilmadi")
        user = get_user(email, db)
        if user.role == Role.SUPERUSER:
            return user
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Foydalanuvchi SuperUser emas")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Qayta Login qilib ko'ring token xatolik")
    
    
def is_admin(token: Annotated[str, Depends(oauth2_scheme)], db : Session = Depends(get_db)):
    """ Admin permission """
    try:
        payload  = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITH])
        email = payload.get("sub")
        user_id = payload.get("id")
        if email is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Foydalanuvchi topilmadi")
        user = get_user(email, db)
        if user.role == Role.ADMIN:
            return user
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Foydalanuvchi Admin emas")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Qayta Login qilib ko'ring token xatolik")
    