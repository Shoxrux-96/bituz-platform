from fastapi import HTTPException, status, Depends

from models import User
from sqlalchemy.orm import Session
from schemas import  users

from utils.hashing import pwd_context
from core.security import authenticate_user


class UserService:
    def __init__(self, db: Session):
        self.db = db


    def get_user(self, user_id: int):
        """ Retrieve user by its id """        
        return self.db.query(User).filter(User.id == user_id).first()


    def get_user_by_tel(self, tel: str):
        """ retrieve user by its tel number""" 
        return self.db.query(User).filter(User.phone_number == tel).first()


    def get_user_by_email(self, email: str):
        """retrieve user by its email""" 
        return self.db.query(User).filter(User.email == email).first()


    def get_all_users(self, skip: int = 0, limit: int = 10):
        """ Retrieve users with pagination.""" 
        return self.db.query(User).offset(skip).limit(limit).all()
    
    
    def create_user(self, user_create: users.RegistrationRequest):
        """ create user by providing email and passowrd , 
            service can be updated later  if some more data is required to register user"""
        
        existance_chek = self.get_user_by_email(user_create.email)
        if existance_chek:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email already exists."
            )
            
        
        hashed_password = pwd_context.hash(user_create.password)
        db_user = User(
            email=user_create.email,
            password=hashed_password,
        )
        self.commit_object(db_user, self.db)
        return db_user


    def update_user(self, user_id: int, user_update: users.UserUpdate):
        """Update user info like email, and password."""

        user_obj = self.get_user(user_id)
        if not user_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )

    
        if user_update.email and user_update.email != user_obj.email:
            existing_user = self.get_user_by_email(user_update.email)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Another user with this email already exists."
                )
            user_obj.email = user_update.email

        if user_update.password is not None:
            user_obj.password = pwd_context.hash(user_update.password)

        return self.commit_object(user_obj, self.db)


    def delete_user(self, user_id: int):
        """ User delete method by its id"""
        user = self.get_user(user_id)
        if not user:
            return None
        self.db.delete(user)
        self.db.commit()
        return user
    
    @staticmethod
    def commit_object(_object_, db):
        db.add(_object_)
        db.commit()
        db.refresh(_object_)
        return _object_



