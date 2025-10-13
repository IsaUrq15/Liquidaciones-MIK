from pydantic import BaseModel
from typing import Optional
from datetime import date

class UsuarioLogin(BaseModel):
    email: str
    password: str

