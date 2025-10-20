#models/afp.py
from core.database import get_connection

class AFPModel:
    @staticmethod
    def get_all():
        conn = get_connection()
        afps = []
        if conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT id, nombre FROM afp")
                afps = cursor.fetchall()
            conn.close()
        return afps