from fastapi import APIRouter, HTTPException
from dto.usuario import UsuarioLogin
from models.usuarios import LoginUser
from typing import List

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

#POST api/v1/usuarios/login
@router.post("/login")
def login(usuario: UsuarioLogin):
    login_model = LoginUser()
    if login_model.authenticate_user(usuario):
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")