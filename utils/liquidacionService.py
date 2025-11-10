# utils/liquidacionService.py - VERSION SIN PRINTS (LIMPIA)

from core.database import get_connection
from datetime import datetime
import traceback


def obtener_datos_empleado(empleado_id: int) -> dict:
    """Obtiene los datos del empleado y sus tasas actuales"""
    conn = get_connection()
    if not conn:
        return None
    
    try:
        with conn.cursor(dictionary=True) as cursor:
            query = """
            SELECT 
                e.id, e.nombres, e.apellidos, e.rut, c.id as contrato_id,
                c.sueldo_base, c.tipo as tipo_contrato, c.estado, c.afp_id,
                c.salud_id, c.afc_id, c.fecha_inicio,
                emp.nombre as empresa_nombre, COALESCE(emp.rut, 'XX.XXX.XXX-X') as empresa_rut,
                COALESCE(emp.direccion, 'Dirección') as empresa_direccion,
                COALESCE(emp.telefono, '0') as empresa_telefono
            FROM empleados e
            JOIN contratos c ON e.id = c.empleado_id
            LEFT JOIN empresas emp ON c.empresa_id = emp.id
            WHERE e.id = %s AND c.estado = 'activo'
            LIMIT 1
            """
            
            cursor.execute(query, (empleado_id,))
            result = cursor.fetchone()
            
            if not result:
                return None
            
            # Obtener tasas vigentes de AFP
            afp_tasa = 10.0
            afp_nombre = "AFP"
            if result['afp_id']:
                cursor.execute("""
                    SELECT afp.nombre, afp_tasas.tasa FROM afp
                    LEFT JOIN afp_tasas ON afp.id = afp_tasas.afp_id
                    WHERE afp.id = %s 
                    AND (afp_tasas.vigente_hasta IS NULL OR afp_tasas.vigente_hasta >= CURDATE())
                    AND afp_tasas.vigente_desde <= CURDATE()
                    ORDER BY afp_tasas.vigente_desde DESC LIMIT 1
                """, (result['afp_id'],))
                afp_result = cursor.fetchone()
                if afp_result:
                    afp_nombre = afp_result['nombre']
                    afp_tasa = float(afp_result['tasa'])
            
            # Obtener tasas vigentes de Salud
            salud_tasa = 7.0
            salud_nombre = "Salud"
            if result['salud_id']:
                cursor.execute("""
                    SELECT salud.nombre, salud_tasas.tasa FROM salud
                    LEFT JOIN salud_tasas ON salud.id = salud_tasas.salud_id
                    WHERE salud.id = %s 
                    AND (salud_tasas.vigente_hasta IS NULL OR salud_tasas.vigente_hasta >= CURDATE())
                    AND salud_tasas.vigente_desde <= CURDATE()
                    ORDER BY salud_tasas.vigente_desde DESC LIMIT 1
                """, (result['salud_id'],))
                salud_result = cursor.fetchone()
                if salud_result:
                    salud_nombre = salud_result['nombre']
                    salud_tasa = float(salud_result['tasa'])
            
            # Obtener tasas vigentes de AFC
            afc_tasa_trabajador = 0.6
            afc_tasa_empleador = 2.4
            afc_nombre = "AFC"
            if result['afc_id']:
                cursor.execute("""
                    SELECT afc.nombre, afc_tasas.tasa_trabajador, afc_tasas.tasa_empleador FROM afc
                    LEFT JOIN afc_tasas ON afc.id = afc_tasas.afc_id
                    WHERE afc.id = %s 
                    AND (afc_tasas.vigente_hasta IS NULL OR afc_tasas.vigente_hasta >= CURDATE())
                    AND afc_tasas.vigente_desde <= CURDATE()
                    ORDER BY afc_tasas.vigente_desde DESC LIMIT 1
                """, (result['afc_id'],))
                afc_result = cursor.fetchone()
                if afc_result:
                    afc_nombre = afc_result['nombre']
                    afc_tasa_trabajador = float(afc_result['tasa_trabajador'])
                    afc_tasa_empleador = float(afc_result['tasa_empleador'])
            
            return {
                "empleado_id": result['id'],
                "empleado_nombre": f"{result['nombres']} {result['apellidos']}",
                "rut": result['rut'],
                "contrato_id": result['contrato_id'],
                "sueldo_base": float(result['sueldo_base']),
                "empresa_nombre": result['empresa_nombre'],
                "empresa_rut": result['empresa_rut'],
                "empresa_direccion": result['empresa_direccion'],
                "empresa_telefono": result['empresa_telefono'],
                "tipo_contrato": result['tipo_contrato'],
                "fecha_inicio": result['fecha_inicio'],
                "afp_tasa": afp_tasa,
                "salud_tasa": salud_tasa,
                "afc_trabajador": afc_tasa_trabajador,
                "afc_empleador": afc_tasa_empleador,
                "afp_nombre": afp_nombre,
                "salud_nombre": salud_nombre,
                "afc_nombre": afc_nombre,
            }
            
    except Exception as e:
        return None
    finally:
        conn.close()


def calcular_liquidacion(datos: dict, horas_extra: int = 0, dias_trabajados: int = 30) -> dict:
    """Calcula la liquidación con la fórmula exacta"""
    
    try:
        # Sueldo proporcional
        sueldo_base = float(datos['sueldo_base']) / 30 * dias_trabajados
        
        # Horas extras
        monto_horas_extra = (((((sueldo_base / 30) * 7) / 44) * 1.5) * horas_extra)
        
        # Imponible sin gratificación
        imponible_sin_gratificacion = sueldo_base + monto_horas_extra
        
        # Gratificación (25%)
        gratificacion = imponible_sin_gratificacion * 0.25
        
        # Total imponible
        total_imponible = imponible_sin_gratificacion + gratificacion
        
        # Descuentos
        afp = total_imponible * float(datos.get('afp_tasa', 0)) / 100
        salud = total_imponible * float(datos.get('salud_tasa', 0)) / 100
        
        # AFC solo para indefinidos
        if datos.get('tipo_contrato', '').upper() == 'PLAZO_FIJO':
            afc = 0
        else:
            afc = total_imponible * float(datos.get('afc_trabajador', 0)) / 100
        
        total_descuentos = afp + salud + afc
        liquido = total_imponible - total_descuentos
        
        return {
            "sueldo_base": round(sueldo_base),
            "horas_extra": int(horas_extra),
            "monto_horas_extra": round(monto_horas_extra),
            "gratificacion": round(gratificacion),
            "total_imponible": round(total_imponible),
            "afp": round(afp),
            "salud": round(salud),
            "afc": round(afc),
            "total_descuentos": round(total_descuentos),
            "liquido": round(liquido)
        }
    
    except Exception as e:
        raise


def guardar_liquidacion_en_bd(
    contrato_id: int, periodo: str, mes: int,
    sueldo_base: float, horas_extra: float = 0,
    gratificacion: float = 0, total_imponible: float = 0,
    total_descuentos: float = 0, liquido_a_pagar: float = 0
) -> bool:
    """Guarda la liquidación en la base de datos"""
    
    conn = get_connection()
    if not conn:
        return False
    
    try:
        with conn.cursor() as cursor:
            year = int(periodo.split('-')[0])
            
            query = """
            INSERT INTO liquidaciones 
            (contrato_id, periodo, mes, sueldo_base, horas_extra, 
             gratificacion, total_imponible, total_descuentos, liquido_a_pagar)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(query, (
                contrato_id, year, mes, sueldo_base, horas_extra,
                gratificacion, total_imponible, total_descuentos, liquido_a_pagar
            ))
            conn.commit()
            return True
            
    except Exception as e:
        conn.rollback()
        return False
    finally:
        conn.close()


def obtener_liquidaciones(empleado_id: int) -> list:
    """Obtiene el historial de liquidaciones de un empleado"""
    
    conn = get_connection()
    if not conn:
        return []
    
    try:
        with conn.cursor(dictionary=True) as cursor:
            query = """
            SELECT l.*, c.sueldo_base FROM liquidaciones l
            JOIN contratos c ON l.contrato_id = c.id
            WHERE c.empleado_id = %s
            ORDER BY l.periodo DESC, l.mes DESC LIMIT 12
            """
            cursor.execute(query, (empleado_id,))
            return cursor.fetchall()
    except Exception:
        return []
    finally:
        conn.close()