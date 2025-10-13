from fastapi import APIRouter, HTTPException
from dto.empleado import EmpleadoCreate, EmpleadoResponse
from models.empleados import EmpleadosModel
from core.mail_service import enviar_correo
from jinja2 import Template
from typing import List

router = APIRouter(prefix="/empleados", tags=["Empleados"])

#GET api/v1/empleados
@router.get("/", response_model=List[EmpleadoResponse])
async def list_empleados():
    asunto = "Correo de prueba"
    body = render_template("Eduardo Onetto", mes_pago="Octubre", contrato_numero="67890")
    await enviar_correo("eduardo.onetto97@gmail.com", asunto, body)
    return EmpleadosModel.get_all()


#POST api/v1/empleados
@router.post("/", response_model=EmpleadoResponse)
def create_empleado(empleado: EmpleadoCreate):
    #ver que llego:
    print(empleado)
    try:
        return EmpleadosModel.create(empleado)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def render_template(nombre_completo: str, empresa="Finantel Group", mes_pago="Septiembre", contrato_numero="12345"):
    with open("templates/email/NotificacionSueldo.html") as f:
        template = Template(f.read())
    return template.render(nombre_completo=nombre_completo, empresa=empresa, mes_pago=mes_pago, contrato_numero=contrato_numero)
