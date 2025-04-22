from fastapi import Request
from passlib.hash import bcrypt
from app.database import SessionLocal
from app.models import User

def authenticate_user(username: str, password: str):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()
    if user and bcrypt.verify(password, user.password_hash):
        return user
    return None

def get_current_user(request: Request):
    user_id = request.session.get("user_id")
    if user_id:
        db = SessionLocal()
        user = db.query(User).filter(User.id == user_id).first()
        db.close()
        return user
    return None

def login_user(request: Request, user: User):
    request.session["user_id"] = user.id

def logout_user(request: Request):
    request.session.clear()