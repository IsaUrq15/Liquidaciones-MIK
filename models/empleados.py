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
    def create(empleado: EmpleadoCreate) -> int | None:
        """
        Inserta un nuevo empleado y retorna el ID generado o None si falla.
        """
        cnx = get_connection()
        if not cnx:
            return None
        cursor = cnx.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO empleados (nombres, apellidos, rut, fecha_nacimiento, direccion)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (empleado.nombres, empleado.apellidos, empleado.rut, empleado.fecha_nacimiento, empleado.direccion),
            )
            cnx.commit()
            new_id = cursor.lastrowid
        except Exception:
            cnx.rollback()
            return None
        finally:
            cursor.close()
            cnx.close()
        return new_id
