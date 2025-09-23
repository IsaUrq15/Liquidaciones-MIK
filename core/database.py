import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        cnx = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="holding_rrhh"
        )
        print("Connection established successfully!")
        return cnx
    except Error as err:
        print(f"Error: {err}")
        return None