import redis
import requests
from decouple import config



ESKIZ_EMAIL = config("ESKIZ_EMAIL")
ESKIZ_PAROL = config("ESKIZ_PAROL")

r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)


def save_otp(phone: str, code: str):
    """
    Yuborilgan OTP kodni redis ga saqlash
    """
    r.setex(f"otp:{phone}", 60, code)


def get_otp(phone: str):
    """
    redisga saqlangnan otp kodni olish
    """
    
    return r.get(f"otp:{phone}")


def loginToEskiz():
    url = "https://notify.eskiz.uz/api/auth/login"
    payload = {
        "email": ESKIZ_EMAIL,
        "password": ESKIZ_PAROL
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post(url, data=payload, headers=headers)
    data = response.json()

    print(response.text)
    if response.status_code == 200:
        token = data['data']['token']
        return token
    return ""
        

def send_sms(phone: str, code: str):
    url = "https://notify.eskiz.uz/api/message/sms/send"
    payload = {
        "mobile_phone": phone,
        "message": "This is test from Eskiz",
        "from": "Bituz"
    }
    headers = {
        "Authorization": f"Bearer {loginToEskiz()}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, json=payload)
    print(response.text)
    return response.ok