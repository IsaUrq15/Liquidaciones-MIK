# routers/liquidaciones.py - VERSION LIMPIA SIN LOGS

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from utils.liquidacionService import obtener_datos_empleado, calcular_liquidacion
from services.pdfService import generar_liquidacion_pdf
from datetime import datetime
import os
import tempfile
import logging

# Configurar logging para desactivar prints
logging.getLogger("utils.liquidacionService").setLevel(logging.CRITICAL)
logging.getLogger("services.pdfService").setLevel(logging.CRITICAL)

router = APIRouter(prefix="/liquidaciones", tags=["liquidaciones"])


# ========== MODELOS ==========
class generar_liquidacion_empleado_id(BaseModel):
    empleado_id: int
    horas_extras: float = 0
    dias_trabajados: int = 30


# ========== ENDPOINTS ==========

@router.post("/{empleado_id}")
def generar_liquidacion_empleado_id(liquidacion: generar_liquidacion_empleado_id):
    """
    Genera liquidación con parámetros: horas extras y días trabajados
    """
    try:
        # Obtener datos del empleado
        datos_empleado = obtener_datos_empleado(liquidacion.empleado_id)
        
        if not datos_empleado:
            raise HTTPException(status_code=404, detail="Empleado no encontrado o sin contrato activo")
        
        # Calcular liquidación
        resultado = calcular_liquidacion(
            datos=datos_empleado,
            horas_extra=int(liquidacion.horas_extras),
            dias_trabajados=liquidacion.dias_trabajados
        )
        
        # Preparar datos para PDF
        empresa_data = {
            "nombre": datos_empleado["empresa_nombre"],
            "rut": datos_empleado["empresa_rut"],
            "direccion": datos_empleado["empresa_direccion"],
            "telefono": datos_empleado["empresa_telefono"],
            "logo_path": "templates/assets/img/logo.png"
        }
        
        # Generar PDF
        temp_dir = tempfile.gettempdir()
        nombre_archivo = f"liquidacion_{datos_empleado['empleado_nombre'].replace(' ', '_')}_{datetime.now().strftime('%d%m%Y_%H%M%S')}.pdf"
        output_path = os.path.join(temp_dir, nombre_archivo)
        
        generar_liquidacion_pdf(
            nombre=datos_empleado["empleado_nombre"],
            rut=datos_empleado["rut"],
            tipo_contrato=datos_empleado["tipo_contrato"],
            datos=resultado,
            empresa=empresa_data,
            sueldo_base_original=float(datos_empleado["sueldo_base"]),
            dias_trabajados=liquidacion.dias_trabajados,
            output_path=output_path
        )
        
        # Guardar liquidación en BD
        try:
            from utils.liquidacionService import guardar_liquidacion_en_bd
            periodo = datetime.now().strftime("%Y-%m")
            mes = datetime.now().month
            
            guardar_liquidacion_en_bd(
                contrato_id=datos_empleado["contrato_id"],
                periodo=periodo,
                mes=mes,
                sueldo_base=resultado["sueldo_base"],
                horas_extra=resultado["monto_horas_extra"],
                gratificacion=resultado["gratificacion"],
                total_imponible=resultado["total_imponible"],
                total_descuentos=resultado["total_descuentos"],
                liquido_a_pagar=resultado["liquido"]
            )
        except Exception:
            pass
        
        # Retornar PDF
        return FileResponse(
            output_path,
            filename=nombre_archivo,
            media_type="application/pdf"
        )
        
    except HTTPException as he:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar liquidación: {str(e)}")


@router.get("/")
def listar_liquidaciones():
    """
    Lista todas las liquidaciones
    """
    try:
        return {"message": "Endpoint para listar liquidaciones"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))