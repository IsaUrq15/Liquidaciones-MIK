#models/afc.py
from core.database import get_connection

class AFCModel:
    @staticmethod
    def get_all():
        conn = get_connection()
        afcs = []
        if conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT id, nombre FROM afc")
                afcs = cursor.fetchall()
            conn.close()
        return afcs