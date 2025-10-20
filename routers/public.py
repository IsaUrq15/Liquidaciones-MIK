from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models.empleados import EmpleadosModel
from models.usuarios import UsuarioModel

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
    usuario_model = UsuarioModel()
    if usuario_model.authenticate_user(email=email, password=password):
        return RedirectResponse(url="/home", status_code=303)
    else:
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "titulo": "Login | Finantel Group",
                "error": "Usuario o contraseña incorrectos"
            }
        )

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
    usuario_model = UsuarioModel()
    usuario_model.create(email=email, password=password, img=img, full_name=full_name)
    return RedirectResponse(url="/", status_code=303)

@router.get("/home", response_class=HTMLResponse)
def home(request: Request):
    empleados = EmpleadosModel.get_all()
    return templates.TemplateResponse("home.html", {"request": request, "empleados": empleados})
