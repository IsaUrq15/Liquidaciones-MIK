from core.database import get_connection
from dto.empleado import EmpleadoCreate, EmpleadoResponse
from typing import List

class EmpleadosModel:

    @staticmethod
    def get_all() -> List[EmpleadoResponse]:
        cnx = get_connection()
        if not cnx:
            return []
        cursor = cnx.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT e.id, e.nombres, e.apellidos, e.rut, e.fecha_nacimiento, e.direccion, "
                "c.empresa_id, c.tipo as tipo_contrato, c.fecha_inicio, c.fecha_termino, "
                "c.sueldo_base, c.afp_id, c.salud_id, c.afc_id "
                "FROM empleados e "
                "JOIN contratos c ON e.id = c.empleado_id"
            )
            empleados = cursor.fetchall()
            # Mapear resultados a modelos Pydantic
            return [EmpleadoResponse(**emp) for emp in empleados]
        finally:
            cursor.close()
            cnx.close()

    @staticmethod
    def create(empleado: EmpleadoCreate) -> EmpleadoResponse:
        cnx = get_connection()
        if not cnx:
            raise Exception("No se pudo conectar a la base de datos")
        cursor = cnx.cursor()
        try:
            # Insertar en empleados
            sql_empleado = """
                INSERT INTO empleados (nombres, apellidos, rut, fecha_nacimiento, direccion)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql_empleado, (
                empleado.nombres, empleado.apellidos, empleado.rut,
                empleado.fecha_nacimiento, empleado.direccion
            ))
            empleado_id = cursor.lastrowid

            # Insertar en contratos
            sql_contrato = """
                INSERT INTO contratos (
                    empleado_id, empresa_id, tipo, fecha_inicio, fecha_termino,
                    sueldo_base, afp_id, salud_id, afc_id
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql_contrato, (
                empleado_id, empleado.empresa_id, empleado.tipo_contrato,
                empleado.fecha_inicio, empleado.fecha_termino,
                empleado.sueldo_base, empleado.afp_id, empleado.salud_id, empleado.afc_id
            ))

            cnx.commit()
            return EmpleadoResponse(id=empleado_id, **empleado.dict())
        except Exception as e:
            print(e)
            cnx.rollback()
            raise e
        finally:
            cursor.close()
            cnx.close()
