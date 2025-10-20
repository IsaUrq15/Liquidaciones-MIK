from pydantic import BaseModel
from typing import Optional
from datetime import date

class LiquidacionCreate(BaseModel):
    nombre: str
    rut: str
    cargo: str
    sueldo_base: float
    horas_extras: float