#models/salud.py
from core.database import get_connection

class SaludModel:
    @staticmethod
    def get_all():
        conn = get_connection()
        saluds = []
        if conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT id, nombre FROM salud")
                saluds = cursor.fetchall()
            conn.close()
        return saluds