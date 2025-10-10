# models/usuarios.py

from core.database import get_connection

class UsuariosModel:
    @staticmethod
    def create(email: str, password: str, img: str, full_name: str) -> int | bool:
        cnx = get_connection()
        if not cnx:
            return False
        cursor = cnx.cursor()
        try:
            sql = """
            INSERT INTO usuarios (email, password, img, full_name, disabled)
            VALUES (%s, %s, %s, %s, 0)
            """
            cursor.execute(sql, (email, password, img, full_name))
            user_id = cursor.lastrowid
            cnx.commit()
            return user_id
        except Exception as e:
            cnx.rollback()
            raise e
        finally:
            cursor.close()
            cnx.close()

    @staticmethod
    def authenticate(email: str, password: str) -> bool:
        cnx = get_connection()
        if not cnx:
            return False
        cursor = cnx.cursor(dictionary=True)
        try:
            sql = "SELECT * FROM usuarios WHERE email = %s AND password = %s AND disabled = 0"
            cursor.execute(sql, (email, password))
            user = cursor.fetchone()
            return user is not None
        finally:
            cursor.close()
            cnx.close()
