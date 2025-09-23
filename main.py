from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from routers import empleados, public

app = FastAPI()

templates = Jinja2Templates(directory="templates")  # apunta a tu carpeta templates

# Rutas privadas 
app.include_router(empleados.router, prefix="/api/v1")
# Rutas públicas
app.include_router(public.router)
