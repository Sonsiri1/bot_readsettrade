from fastapi import APIRouter, Depends
from requests import Session
from schemas.user_schema import UserRegister
from schemas.user_schema import UserLogin
import services.user_service as user_service
from core.database import get_db
from fastapi import HTTPException

router = APIRouter()

@router.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    return user_service.register_user(
        db,
        user.username,
        user.password_hash
    )

@router.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    user_login = user_service.login_user(db, user.username, user.password)

    if not user_login:
        raise HTTPException(
            status_code=401,
            detail="ไม่สามารถเข้าสู่ระบบได้"
        )
    
    return user_login