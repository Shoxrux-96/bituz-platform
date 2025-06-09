import random
from fastapi import APIRouter, HTTPException, Depends
from services.auth_service import UserService
from schemas.users import EmailRequest, RegistrationRequest

from fastapi.security import OAuth2PasswordRequestForm
from utils._otp import save_otp, send_sms, get_otp
from utils.email_otp import send_email
from utils.jwt import create_access_token, create_refresh_token, verify_jwt_token

from sqlalchemy.orm import Session
from core.database import get_db
from core.security import authenticate_user


route = APIRouter(tags=["Auth & OTP"])


# @route.post("/verify-id/")
# async def verify_id(file: UploadFile = File(...)):
#     image_bytes = await file.read()
#     image = Image.open(io.BytesIO(image_bytes))
    
#     # Extract text using Tesseract
#     extracted_text = pytesseract.image_to_string(image)

#     # Simple keyword check (improve this logic with regex or parsing)
#     if "PASSPORT" in extracted_text.upper() or "ID CARD" in extracted_text.upper():
#         return {"status": "verified", "text": extracted_text}
#     return {"status": "unverified", "text": extracted_text}


# @route.post("/users/verify-phone", description="Phone verification endpoint by OTP")
# def verify_phone(request: PhoneRequest):
#     code = str(random.randint(100000, 999999))
#     save_otp(request.phone_number, "This is test from Eskiz")
    
#     if send_sms(request.phone_number, code):
#         return {"message": f"Verification code sent to {request.phone_number}"}
    
#     raise HTTPException(status_code=500, detail="Failed to send SMS")



@route.post("/users/verify-email", description="Email verification endpoint by OTP")
def verify_phone(request: EmailRequest):
    code = str(random.randint(100000, 999999))
    save_otp(request.email, code)
    
    if send_email(request.email, code):
        return {"message": f"Verification code sent to {request.email}"}
    
    raise HTTPException(status_code=500, detail="Failed to send email")


@route.post("/users/register")
def register_user(request: RegistrationRequest,db: Session = Depends(get_db)):
    stored_code = get_otp(request.email)
    if stored_code is None or stored_code != request.verification_code:
        raise HTTPException(status_code=400, detail="Email not verified")
    
    user_serv = UserService(db)
    user = user_serv.create_user(request)
    return {"message": "User registered successfully"}


@route.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    user_serv = UserService(db)
    user = user_serv.get_user_by_email(form_data.username)

    if not user or not authenticate_user(form_data.username, form_data.password, db):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@route.post("/refresh/token")
def refresh_token(refresh_token: str):
    payload = verify_jwt_token(refresh_token)
    phone_number = payload.get("sub")
    new_access_token = create_access_token(data={"sub": phone_number})
    return {"access_token": new_access_token}