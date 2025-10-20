from core.database import get_connection
from dto.usuario import UsuarioLogin
import bcrypt

class LoginUser:
    def hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

    def authenticate_user(self, email: str, password: str) -> bool:
        cnx = get_connection()
        if not cnx:
            return False
        cursor = cnx.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
            user = cursor.fetchone()
            if user and self.verify_password(password, user['password']):
                return True
            return False
        finally:
            cursor.close()
            cnx.close()

    def create(self, email: str, password: str, img: str, full_name: str) -> bool:
        cnx = get_connection()
        if not cnx:
            return False
        hashed_password = self.hash_password(password)
        cursor = cnx.cursor()
        try:
            cursor.execute(
                "INSERT INTO usuarios (email, password, img, full_name) VALUES (%s, %s, %s, %s)",
                (email, hashed_password, img, full_name)
            )
            cnx.commit()
            return True
        except Exception as e:
            print("Error creando usuario:", e)
            cnx.rollback()
            return False
        finally:
            cursor.close()
            cnx.close()
