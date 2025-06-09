from pydantic import BaseModel, EmailStr


class EmailRequest(BaseModel):
    email: EmailStr
    class Config:
        from_attributes = True


class RegistrationRequest(BaseModel):
    email: EmailStr
    password: str
    verification_code: str


class UserUpdate(BaseModel):
    email: EmailStr
    password: str
    class Config:
        from_attributes = True
