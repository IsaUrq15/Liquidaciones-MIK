# routers/empleados.py - ENDPOINTS CORREGIDOS Y FUNCIONABLES

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from core.database import get_connection
from datetime import datetime

router = APIRouter(prefix="/empleados", tags=["empleados"])


# ========== MODELOS PYDANTIC ==========
class EmpleadoCreate(BaseModel):
    nombres: str
    apellidos: str
    rut: str
    fecha_nacimiento: str
    direccion: str
    empresa_id: int
    afp_id: int
    salud_id: int
    tipo_contrato: str
    fecha_ingreso: str
    sueldo_base: int


# ========== ENDPOINTS CRUD ==========

@router.post("/crear")
def crear_empleado(empleado: EmpleadoCreate):
    """
    Crea un nuevo empleado y su contrato
    """
    try:
        conn = get_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Error de conexión a BD")

        with conn.cursor() as cursor:
            # 1. Insertar empleado
            query_empleado = """
            INSERT INTO empleados (nombres, apellidos, rut, fecha_nacimiento, direccion)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query_empleado, (
                empleado.nombres,
                empleado.apellidos,
                empleado.rut,
                empleado.fecha_nacimiento,
                empleado.direccion
            ))
            empleado_id = cursor.lastrowid

            # 2. Insertar contrato
            query_contrato = """
            INSERT INTO contratos 
            (empleado_id, empresa_id, tipo, fecha_inicio, sueldo_base, afp_id, salud_id, afc_id, estado)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'activo')
            """
            cursor.execute(query_contrato, (
                empleado_id,
                empleado.empresa_id,
                empleado.tipo_contrato,
                empleado.fecha_ingreso,
                empleado.sueldo_base,
                empleado.afp_id,
                empleado.salud_id,
                1  # afc_id por defecto
            ))

            conn.commit()
            
            return {
                "id": empleado_id,
                "message": f"Empleado {empleado.nombres} creado exitosamente"
            }

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error al crear empleado: {str(e)}")
    finally:
        if conn:
            conn.close()


@router.get("/")
def listar_empleados() -> List[dict]:
    """
    Lista todos los empleados con su información de contrato
    """
    try:
        conn = get_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Error de conexión a BD")

        with conn.cursor(dictionary=True) as cursor:
            query = """
            SELECT 
                e.id,
                e.nombres,
                e.apellidos,
                e.rut,
                e.fecha_nacimiento,
                e.direccion,
                c.id as contrato_id,
                c.sueldo_base,
                c.tipo as tipo_contrato,
                c.estado,
                emp.nombre as empresa_nombre,
                afp.nombre as afp_nombre,
                salud.nombre as salud_nombre
            FROM empleados e
            LEFT JOIN contratos c ON e.id = c.empleado_id
            LEFT JOIN empresas emp ON c.empresa_id = emp.id
            LEFT JOIN afp ON c.afp_id = afp.id
            LEFT JOIN salud ON c.salud_id = salud.id
            ORDER BY e.id DESC
            """
            cursor.execute(query)
            result = cursor.fetchall()
            
            return result if result else []

    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al obtener empleados")
    finally:
        conn.close()


@router.get("/{empleado_id}")
def obtener_empleado(empleado_id: int):
    """
    Obtiene información detallada de un empleado
    """
    try:
        conn = get_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Error de conexión a BD")

        with conn.cursor(dictionary=True) as cursor:
            query = """
            SELECT 
                e.*,
                c.id as contrato_id,
                c.sueldo_base,
                c.tipo as tipo_contrato,
                c.estado,
                emp.nombre as empresa_nombre,
                afp.nombre as afp_nombre,
                salud.nombre as salud_nombre
            FROM empleados e
            LEFT JOIN contratos c ON e.id = c.empleado_id
            LEFT JOIN empresas emp ON c.empresa_id = emp.id
            LEFT JOIN afp ON c.afp_id = afp.id
            LEFT JOIN salud ON c.salud_id = salud.id
            WHERE e.id = %s
            LIMIT 1
            """
            cursor.execute(query, (empleado_id,))
            result = cursor.fetchone()
            
            if not result:
                raise HTTPException(status_code=404, detail="Empleado no encontrado")
            
            return result

    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al obtener empleado")
    finally:
        conn.close()


# ========== ENDPOINTS PARA CARGAS DINÁMICAS ==========

@router.get("/data/empresas")
def obtener_empresas() -> List[dict]:
    """
    Obtiene listado de empresas para selector
    """
    try:
        conn = get_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Error de conexión a BD")

        with conn.cursor(dictionary=True) as cursor:
            print("Obteniendo empresas...")
            cursor.execute("SELECT id, nombre FROM empresas ORDER BY nombre")
            result = cursor.fetchall()
            print(f"Empresas encontradas: {len(result)}")
            return result if result else []

    except Exception as e:
        print(f"Error al obtener empresas: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al obtener empresas")
    finally:
        conn.close()


@router.get("/data/afps")
def obtener_afps() -> List[dict]:
    """
    Obtiene listado de AFPs para selector
    """
    try:
        conn = get_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Error de conexión a BD")

        with conn.cursor(dictionary=True) as cursor:
            print("Obteniendo AFPs...")
            cursor.execute("SELECT id, nombre FROM afp ORDER BY nombre")
            result = cursor.fetchall()
            print(f"AFPs encontradas: {len(result)}")
            return result if result else []

    except Exception as e:
        print(f"Error al obtener AFPs: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al obtener AFPs")
    finally:
        conn.close()


@router.get("/data/salud")
def obtener_salud() -> List[dict]:
    """
    Obtiene listado de instituciones de salud para selector
    """
    try:
        conn = get_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Error de conexión a BD")

        with conn.cursor(dictionary=True) as cursor:
            print("Obteniendo Salud...")
            cursor.execute("SELECT id, nombre FROM salud ORDER BY nombre")
            result = cursor.fetchall()
            print(f"Instituciones salud encontradas: {len(result)}")
            return result if result else []

    except Exception as e:
        print(f"Error al obtener salud: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al obtener salud")
    finally:
        conn.close()