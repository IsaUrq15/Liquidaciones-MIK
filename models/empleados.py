
# models/empleados.py
from core.database import get_connection
from typing import List
from datetime import date
from pydantic import BaseModel, Field, ConfigDict
from typing_extensions import Annotated
from annotated_types import MinLen, MaxLen



class EmpleadoBase(BaseModel):
    nombres: Annotated[str, MinLen(1)] = Field(..., description="Nombres del empleado")
    apellidos: Annotated[str, MinLen(1)] = Field(..., description="Apellidos del empleado")
    rut: Annotated[str, MinLen(1), MaxLen(12)] = Field(..., description="RUT del empleado")
    fecha_nacimiento: date = Field(..., description="Fecha de nacimiento")
    direccion: Annotated[str, MinLen(1)] = Field(..., description="Dirección del empleado")

    model_config = ConfigDict(from_attributes=True)


class EmpleadoCreate(EmpleadoBase):
    pass


class EmpleadoInDB(EmpleadoBase):
    id: int = Field(..., description="ID del empleado")


class EmpleadosModel:
    @staticmethod
    def get_all() -> List[EmpleadoInDB]:
        cnx = get_connection()
        if not cnx:
            return []
        cursor = cnx.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT id, nombres, apellidos, rut, fecha_nacimiento, direccion FROM empleados"
            )
            empleados = cursor.fetchall()
        finally:
            cursor.close()
            cnx.close()
        return [EmpleadoInDB(**emp) for emp in empleados]


@staticmethod
def create(
    nombres: str, apellidos: str, rut: str, fecha_nacimiento: str, direccion: str,
    empresa_id: int, tipo_contrato: str, fecha_inicio: str, fecha_termino: str,
    sueldo_base: float, afp_id: int, salud_id: int, afc_id: int
) -> int | bool:
    cnx = get_connection()
    if not cnx:
        return False
    cursor = cnx.cursor()
    try:
  
        sql_empleado = """
        INSERT INTO empleados (nombres, apellidos, rut, fecha_nacimiento, direccion)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql_empleado, (nombres, apellidos, rut, fecha_nacimiento, direccion))
        empleado_id = cursor.lastrowid

       
        sql_contrato = """
        INSERT INTO contratos (
            empleado_id, empresa_id, tipo, fecha_inicio, fecha_termino,
            sueldo_base, afp_id, salud_id, afc_id
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql_contrato, (
            empleado_id, empresa_id, tipo_contrato, fecha_inicio,
            fecha_termino, sueldo_base, afp_id, salud_id, afc_id
        ))

        cnx.commit()
        return empleado_id

    except Exception as e:
        cnx.rollback()
        raise e

    finally:
        cursor.close()
        cnx.close()
