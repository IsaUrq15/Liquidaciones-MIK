from core.database import get_connection

class EmpleadosModel:
    @staticmethod
    def get_all():
        cnx = get_connection()
        if not cnx:
            return []
        cursor = cnx.cursor(dictionary=True)
        cursor.execute("SELECT id, username, email FROM empleados")
        empleados = cursor.fetchall()
        cursor.close()
        cnx.close()
        return empleados

    @staticmethod
    def create(username: str, email: str):
        cnx = get_connection()
        if not cnx:
            return False
        cursor = cnx.cursor()
        cursor.execute(
            "INSERT INTO empleados (username, email) VALUES (%s, %s)",
            (username, email)
        )
        cnx.commit()
        cursor.close()
        cnx.close()
        return True