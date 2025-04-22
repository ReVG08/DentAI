from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", name="home")
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@router.get("/about", name="about")
def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@router.get("/contact", name="contact")
def contact(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request, "submitted": False})