from fastapi import APIRouter, HTTPException
from models.empleados import EmpleadosModel

router = APIRouter(prefix="/empleados", tags=["Empleados"])

@router.get("/")
def list_empleados():
    empleados = EmpleadosModel.get_all()
    return empleados

@router.post("/")
def create_empleado(username: str, email: str):
    #Campos Obligatorios:
    campos_obligatorios = [email]
    if not all(campos_obligatorios):
        raise HTTPException(status_code=400, detail="Todos los campos son obligatorios")
        
    #Crear empleado:
    success = EmpleadosModel.create(username, email)
    if not success:
        raise HTTPException(status_code=500, detail="Empleado could not be created")
    return {"message": "Empleado created successfully"}
