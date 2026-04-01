from fastapi import APIRouter, Depends, Request, HTTPException, Response
from requests import Session
from schemas.user_schema import UserRegister
from schemas.user_schema import UserLogin
import services.user_service as user_service
from core.database import get_db
from fastapi import HTTPException
from jose import jwt, JWTError

router = APIRouter()

@router.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    return user_service.register_user(
        db,
        user.username,
        user.password
    )

@router.post("/login")
def login_user(user: UserLogin, response: Response, db: Session = Depends(get_db)):
    user_login = user_service.login_user(db, user.username, user.password)

    if not user_login:
        raise HTTPException(
            status_code=401,
            detail="ไม่สามารถเข้าสู่ระบบได้"
        )
    token = user_login["token"]

    # set cookie
    response.set_cookie(
        key="jwt",
        value=token,
        httponly=True,
        samesite="lax",
        secure=False  # localhost ใช้ False
    )

    return {
        "msg": "login success"
    }

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

def verify_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None


@router.get("/auth/me")
async def get_me(request: Request):
    token = None

    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]

    if not token:
        token = request.cookies.get("jwt")

    if not token:
        raise HTTPException(status_code=401, detail="No token")

    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    return {
        "username": payload.get("sub"),
    }

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("jwt")
    return {"msg": "logout success"}