# routers/public.py

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models.empleados import EmpleadosModel
from models.usuarios import UsuariosModel

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "titulo": "Login | Finantel Group"})

@router.post("/", response_class=HTMLResponse)
async def login_post(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):
    # Lógica de validación de login puede ir aquí
    return RedirectResponse(url="/home", status_code=303)

@router.get("/registro", response_class=HTMLResponse)
def registro(request: Request):
    return templates.TemplateResponse("registrologin.html", {"request": request, "titulo": "Registro | Finantel Group"})

@router.post("/registro")
async def crear_usuario(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    img: str = Form(...),
    full_name: str = Form(...)
):
    UsuariosModel.create(email=email, password=password, img=img, full_name=full_name)
    return RedirectResponse(url="/", status_code=303)

@router.get("/home", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "titulo": "Home | Finantel Group"})
#    return templates.TemplateResponse("home.html",  {"request": request, "empleados": empleados}) para tirar el listado de empleados

@router.get("/lista", response_class=HTMLResponse)
def lista(request: Request):
    empleados = EmpleadosModel.get_all()
    return templates.TemplateResponse("lista.html", {"request": request, "empleados": empleados})
