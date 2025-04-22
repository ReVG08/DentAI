from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from passlib.hash import bcrypt
from app.auth import get_current_user
from app.database import SessionLocal
from app.models import User

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/admin")
def admin_panel(request: Request):
    user = get_current_user(request)
    if not user or not user.is_admin:
        return RedirectResponse("/", status_code=302)
    db = SessionLocal()
    users = db.query(User).all()
    db.close()
    return templates.TemplateResponse("admin.html", {"request": request, "users": users})

@router.post("/admin/create_user")
def create_user(request: Request, username: str = Form(...), password: str = Form(...), user_type: str = Form(...)):
    user = get_current_user(request)
    if not user or not user.is_admin:
        return RedirectResponse("/", status_code=302)
    db = SessionLocal()
    new_user = User(
        username=username,
        password_hash=bcrypt.hash(password),
        is_admin=(user_type == "admin"),
        user_type=user_type
    )
    db.add(new_user)
    db.commit()
    db.close()
    return RedirectResponse("/admin", status_code=302)

@router.post("/admin/bind_api_key")
def bind_api_key(request: Request, user_id: int = Form(...), api_key: str = Form(...)):
    user = get_current_user(request)
    if not user or not user.is_admin:
        return RedirectResponse("/", status_code=302)
    db = SessionLocal()
    acc = db.query(User).filter(User.id == user_id).first()
    if acc:
        acc.openai_api_key = api_key
        db.commit()
    db.close()
    return RedirectResponse("/admin", status_code=302)