from core.database import get_connection
from datetime import date

class EmpleadosModel:
    @staticmethod
    def get_all():
        """
        Recupera todos los empleados registrados con sus datos completos.
        """
        cnx = get_connection()
        if not cnx:
            return []
        try:
            with cnx.cursor(dictionary=True) as cursor:
                cursor.execute(
                    "SELECT id, nombres, apellidos, rut, fecha_nacimiento, direccion FROM empleados"
                )
                return cursor.fetchall()
        finally:
            cnx.close()

    @staticmethod
    def create(nombres: str, apellidos: str, rut: str, fecha_nacimiento: date, direccion: str):
        """
        Inserta un empleado en la base de datos.
        Retorna el ID generado o None si falla.
        """
        cnx = get_connection()
        if not cnx:
            return None
        try:
            with cnx.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO empleados (nombres, apellidos, rut, fecha_nacimiento, direccion)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (nombres, apellidos, rut, fecha_nacimiento, direccion),
                )
                cnx.commit()
                new_id = cursor.lastrowid
                return new_id
        except Exception:
            cnx.rollback()
            return None
        finally:
            cnx.close()
