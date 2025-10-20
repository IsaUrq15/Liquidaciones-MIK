from core.database import get_connection

class EmpresasModel:
    @staticmethod
    def get_all():
        conn = get_connection()
        empresas = []
        if conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT id, nombre FROM empresas")
                empresas = cursor.fetchall()
            conn.close()
        return empresas
