from pydantic import BaseModel
from typing import Optional
from datetime import date

class LiquidacionCreate(BaseModel):
    nombre: str
    rut: str
    tipo_contrato: str
    sueldo_base: float
    horas_extras: float