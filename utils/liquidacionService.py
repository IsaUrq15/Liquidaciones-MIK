import mysql.connector
import datetime


def calcular_liquidacion_simple(sueldo_base: float, horas_extras: float, inm: float = 529000) -> dict:
    # Gratificación legal (25% del sueldo con tope)
    tope_gratificacion = (4.75 * inm) / 12
    gratificacion = min(sueldo_base * 0.25, tope_gratificacion)

    horas_extras_calc = (((((sueldo_base / 30) * 7) / 44) * 1.5) * horas_extras)
    total_haberes = sueldo_base + horas_extras_calc + gratificacion

    afp = sueldo_base * 0.10     # 10%
    afc = sueldo_base * 0.006    # 0.6%
    salud = sueldo_base * 0.07   # 7%

    total_descuentos = afp + afc + salud
    liquido = total_haberes - total_descuentos

    return {
        "sueldo_base": sueldo_base,
        "horas_extras": horas_extras_calc,
        "gratificacion": gratificacion,
        "total_haberes": total_haberes,
        "afp": afp,
        "afc": afc,
        "salud": salud,
        "total_descuentos": total_descuentos,
        "liquido": liquido
    }


def obtener_datos_empleado(empleado_id):
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='holding_rrhh'
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
    SELECT c.id as contrato_id, c.sueldo_base,
           e.nombres as empleado_nombre,
           e.rut as rut,
           em.nombre as empresa_nombre,
           em.rut as empresa_rut,
           em.direccion as empresa_direccion,
           em.telefono as empresa_telefono,       
           c.tipo as tipo_contrato,
           afp.nombre as afp_nombre, aft.tasa as afp_tasa,
           sa.nombre as salud_nombre, sat.tasa as salud_tasa,
           afc.nombre as afc_nombre, afct.tasa_trabajador as afc_tasa
    FROM contratos c
    JOIN empleados e ON c.empleado_id = e.id
    JOIN empresas em ON c.empresa_id = em.id
    JOIN afp ON c.afp_id = afp.id
    JOIN afp_tasas aft ON c.afp_id = aft.afp_id
    JOIN salud sa ON c.salud_id = sa.id
    JOIN salud_tasas sat ON sa.id = sat.salud_id
    JOIN afc ON c.afc_id = afc.id
    JOIN afc_tasas afct ON afc.id = afct.afc_id
    WHERE e.id=%s AND c.estado='activo'
    LIMIT 1
""", (empleado_id,))
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()
    return resultado


def calcular_liquidacion(sueldo_base, afp_tasa, salud_tasa, afc_tasa):
    descuentos = {
        'afp': sueldo_base * afp_tasa / 100,
        'salud': sueldo_base * salud_tasa / 100,
        'afc': sueldo_base * afc_tasa / 100
    }
    total_descuentos = sum(descuentos.values())
    sueldo_liquido = sueldo_base - total_descuentos
    return {
        'sueldo_base': sueldo_base,
        'descuentos': descuentos,
        'total_descuentos': total_descuentos,
        'sueldo_liquido': sueldo_liquido,
        'horas_extra': 0,
        'gratificacion': 0,
        'total_imponible': sueldo_base
    }


def guardar_liquidacion_en_bd(contrato_id, periodo, mes, sueldo_base,
                              horas_extra, gratificacion, total_imponible,
                              total_descuentos, liquido_a_pagar):
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='holding_rrhh'
    )
    cursor = conn.cursor()
    try:
        sql = """
        INSERT INTO liquidaciones (
            contrato_id, periodo, mes, sueldo_base, horas_extra, gratificacion,
            total_imponible, total_descuentos, liquido_a_pagar
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            contrato_id, periodo, mes, sueldo_base,
            horas_extra, gratificacion, total_imponible,
            total_descuentos, liquido_a_pagar
        )
        cursor.execute(sql, params)
        conn.commit()
        return True
    except Exception as e:
        print("Error al guardar liquidación:", e)
        return False
    finally:
        cursor.close()
        conn.close()