from fastapi import APIRouter, HTTPException
from datetime import date
from typing import Optional
from pydantic import BaseModel, Field
from models.empleados import EmpleadosModel


router = APIRouter(prefix="/empleados", tags=["Empleados"])


class EmpleadoCreateRequest(BaseModel):
    nombres: str = Field(..., min_length=1)
    apellidos: str = Field(..., min_length=1)
    rut: str = Field(..., min_length=1, max_length=12)
    fecha_nacimiento: date
    direccion: str = Field(..., min_length=1)


@router.get("/")
def list_empleados():
    empleados = EmpleadosModel.get_all()
    return empleados


@router.post("/")
def create_empleado(empleado: EmpleadoCreateRequest):
    # Validación automática con Pydantic asegura que todos los campos están presentes y bien formateados
    
    new_id = EmpleadosModel.create(
        empleado.nombres,
        empleado.apellidos,
        empleado.rut,
        empleado.fecha_nacimiento,
        empleado.direccion
    )
    if not new_id:
        raise HTTPException(status_code=500, detail="Empleado no pudo ser creado")
    return {"message": "Empleado creado exitosamente", "id": new_id}