
from core.database import get_connection

def crear_contrato_por_empleado(empleado_id: int) -> bool:
    cnx = get_connection()
    if not cnx:
        return False
    cursor = cnx.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO contratos (empleado_id, empresa_id, tipo, fecha_inicio, sueldo_base, afp_id, salud_id, afc_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,    
        )
        cnx.commit()
    except Exception:
        cnx.rollback()
        cursor.close()
        cnx.close()
        return False
    cursor.close()
    cnx.close()
    return True

