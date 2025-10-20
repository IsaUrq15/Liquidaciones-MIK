from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from routers import empleados, public, usuarios, liquidaciones
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "*",  # Permite todas las fuentes (dominios)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all standard methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)

app.mount(
    "/assets",  
    StaticFiles(directory="templates/assets"),
    name="assets"
)
templates = Jinja2Templates(directory="templates")  

# Rutas privadas 
app.include_router(empleados.router, prefix="/api/v1")
app.include_router(usuarios.router, prefix="/api/v1")

app.include_router(liquidaciones.router, prefix="/api/v1")

# Rutas públicas
app.include_router(public.router)


