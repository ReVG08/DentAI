from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from app.routes import home, auth, admin, dentist

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="super-secret-key")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/static/uploads", StaticFiles(directory="app/uploads"), name="uploads")
templates = Jinja2Templates(directory="app/templates")

app.include_router(home.router)
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(dentist.router)