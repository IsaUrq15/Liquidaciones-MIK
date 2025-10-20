from fastapi import APIRouter, HTTPException
from dto.usuario import UsuarioLogin
from models.usuarios import UsuarioModel

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.post("/login")
def login(usuario: UsuarioLogin):
    usuario_model = UsuarioModel()
    if usuario_model.authenticate_user(usuario):
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
