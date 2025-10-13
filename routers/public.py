# routers/public.py
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models.empleados import EmpleadosModel

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Página de inicio
@router.get("/", response_class=HTMLResponse)
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "titulo": "Login | Finantel Group"})

# Página de login
@router.get("/home", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "titulo": "Home | Finantel Group"})

# Página de empleados
@router.get("/empleados", response_class=HTMLResponse)
def empleados(request: Request):
    return templates.TemplateResponse("empleados.html", {"request": request, "titulo": "Empleados | Finantel Group", "empleados": EmpleadosModel.get_all()})