from core.database import get_connection
from datetime import date


def crear_contrato_por_empleado(
    empleado_id: int,
    empresa_id: int,
    tipo: str,
    fecha_inicio: date,
    sueldo_base: float,
    afp_id: int,
    salud_id: int,
    afc_id: int,
) -> bool:
    """
    Crea un contrato asociado a un empleado con los parámetros indicados.
    Retorna True si la operación fue exitosa, False en caso contrario.
    """
    cnx = get_connection()
    if not cnx:
        return False
    try:
        with cnx.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO contratos 
                (empleado_id, empresa_id, tipo, fecha_inicio, sueldo_base, afp_id, salud_id, afc_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (empleado_id, empresa_id, tipo, fecha_inicio, sueldo_base, afp_id, salud_id, afc_id),
            )
        cnx.commit()
        return True
    except Exception:
        cnx.rollback()
        return False
    finally:
        cnx.close()