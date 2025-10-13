from core.database import get_connection
from dto.usuario import UsuarioLogin
from typing import List

class LoginUser:
    
    def authenticate_user(self, usuario: UsuarioLogin) -> bool:
        cnx = get_connection()
        if not cnx:
            return []
        cursor = cnx.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (usuario.email,))
        user = cursor.fetchone()
        if user and user['password'] == usuario.password:
            return True
        return False