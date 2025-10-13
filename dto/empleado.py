from pydantic import BaseModel
from typing import Optional
from datetime import date

class EmpleadoCreate(BaseModel):
    nombres: str
    apellidos: str
    rut: str
    fecha_nacimiento: date
    direccion: str
    empresa_id: int
    tipo_contrato: str
    fecha_inicio: date
    fecha_termino: Optional[date] = None
    sueldo_base: float
    afp_id: int
    salud_id: int
    afc_id: Optional[int] = None

    

class EmpleadoResponse(EmpleadoCreate):
    id: int
