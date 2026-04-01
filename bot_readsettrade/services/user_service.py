import os

import bcrypt
from models.user_model import User
from fastapi import HTTPException
from jose import jwt

def register_user(db, username, password):
    # check ซ้ำ
    existing = db.query(User).filter(User.username == username).first()
    if existing:
        raise HTTPException(status_code=400, detail="username ซ้ำ")

    # hash
    hashed = bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')

    user = User(
        username=username,
        password_hash=hashed
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

from datetime import datetime, timedelta

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

def create_token(data: dict):
    to_encode = data.copy()
    to_encode["exp"] = datetime.utcnow() + timedelta(hours=2)
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
def login_user(db, username, password):
    user = db.query(User).filter(User.username == username).first()

    if not user:
        return None

    if not bcrypt.checkpw(
        password.encode('utf-8'),
        user.password_hash.encode('utf-8')
    ):
        return None

    token = create_token({
        "sub": user.username
    })

    return {
        "username": user.username,
        "token": token   # ✅ ใช้ชื่อเดียว
    }