from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models.empleados import EmpleadosModel  # Nota la S en EmpleadosModel

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "titulo": "Login | Finantel Group"})

@router.get("/home", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "titulo": "Home | Finantel Group"})

@router.get("/lista", response_class=HTMLResponse)
def lista(request: Request):
    empleados = EmpleadosModel.get_all()  # Corregido aquí: EmpleadosModel
    return templates.TemplateResponse("lista.html", {"request": request, "empleados": empleados})
