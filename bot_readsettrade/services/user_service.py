import bcrypt
from models.user_model import User
from fastapi import HTTPException

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

def login_user(db, username, password):
    user = db.query(User).filter(User.username == username).first()

    if not user:
        return None

    try:
        if not bcrypt.checkpw(
            password.encode('utf-8'),
            user.password_hash.encode('utf-8')
        ):
            return None
    except Exception as e:
        print("bcrypt error:", e)
        return None

    return {
        "username": user.username,
        "token": "fake-token"
    }