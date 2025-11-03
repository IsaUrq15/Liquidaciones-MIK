from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import FileResponse
from dto.liquidacion import LiquidacionCreate
from utils.liquidacionService import obtener_datos_empleado, calcular_liquidacion, guardar_liquidacion_en_bd, calcular_liquidacion_simple
from services.pdfService import generar_liquidacion_pdf
import os
import tempfile
import datetime

router = APIRouter(prefix="/liquidaciones", tags=["liquidacion"])


@router.post("/generar", response_class=FileResponse)
def crear_liquidacion_manual(liquidacion: LiquidacionCreate):
    try:
        # Usar cálculo simple para el endpoint manual
        datos = calcular_liquidacion_simple(
            liquidacion.sueldo_base,
            liquidacion.horas_extras
        )

        empresa = {
            "nombre": "Finantel Group SpA",
            "rut": "77.123.456-7",
            "direccion": "Av. Los Leones 1234, Santiago",
            "telefono": "+56 9 8765 4321",
            "logo_path": os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    "..",
                    "templates", "assets", "img", "logo.png"
                )
            )
        }

        if not os.path.exists(empresa["logo_path"]):
            raise HTTPException(status_code=404, detail=f"Logo no encontrado en {empresa['logo_path']}")

        pdf_path = os.path.join(tempfile.gettempdir(), f"liquidacion_{liquidacion.nombre.replace(' ', '_')}.pdf")
        generar_liquidacion_pdf(
            nombre=liquidacion.nombre,
            rut=liquidacion.rut,
            tipo_contrato=liquidacion.tipo_contrato,
            datos=datos,
            empresa=empresa,
            output_path=pdf_path
        )

        return FileResponse(
            path=pdf_path,
            media_type="application/pdf",
            filename=f"liquidacion_{liquidacion.nombre.replace(' ', '_')}.pdf"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{empleado_id}")
def generar_liquidacion_get(empleado_id: int):
    datos = obtener_datos_empleado(empleado_id)
    if not datos:
        raise HTTPException(status_code=404, detail="Empleado no tiene contrato activo o no existe")

    resultado = calcular_liquidacion(
        datos["sueldo_base"],
        datos["afp_tasa"],
        datos["salud_tasa"],
        datos["afc_tasa"]
    )

    exito = guardar_liquidacion_en_bd(
        datos["contrato_id"],
        periodo=datetime.date.today().strftime("%Y-%m"),
        mes=datetime.date.today().month,
        sueldo_base=resultado["sueldo_base"],
        horas_extra=resultado["horas_extra"],
        gratificacion=resultado.get("gratificacion", 0),
        total_imponible=resultado.get("total_imponible", resultado["sueldo_base"]),
        total_descuentos=resultado["total_descuentos"],
        liquido_a_pagar=resultado.get("sueldo_liquido", 0)
    )

    if not exito:
        raise HTTPException(status_code=500, detail="Error al guardar la liquidación")

    return {
        "empleado_nombre": datos["empleado_nombre"],
        "empresa_nombre": datos["empresa_nombre"],
        "tipo_contrato": datos["tipo_contrato"],
        "sueldo_base": resultado["sueldo_base"],
        "descuentos": resultado["descuentos"],
        "total_descuentos": resultado["total_descuentos"],
        "sueldo_liquido": resultado.get("sueldo_liquido", 0)
    }


@router.post("/generar_con_empleado_id", response_class=FileResponse)
def generar_liquidacion_post(empleado_id: int = Body(..., embed=True)):
    datos = obtener_datos_empleado(empleado_id)
    if not datos:
        raise HTTPException(status_code=404, detail="Empleado no tiene contrato activo o no existe")

    resultado = calcular_liquidacion(
        datos["sueldo_base"],
        datos["afp_tasa"],
        datos["salud_tasa"],
        datos["afc_tasa"]
    )
    print(resultado)

    exito = guardar_liquidacion_en_bd(
        datos["contrato_id"],
        periodo=datetime.date.today().strftime("%Y-%m"),
        mes=datetime.date.today().month,
        sueldo_base=resultado["sueldo_base"],
        horas_extra=resultado["horas_extra"],
        gratificacion=resultado.get("gratificacion", 0),
        total_imponible=resultado.get("total_imponible", resultado["sueldo_base"]),
        total_descuentos=resultado["total_descuentos"],
        liquido_a_pagar=resultado.get("sueldo_liquido", 0)
    )

    if not exito:
        raise HTTPException(status_code=500, detail="Error al guardar la liquidación")

    pdf_filename = f"liquidacion_{datos['empleado_nombre'].replace(' ', '_')}_{datetime.date.today().month}.pdf"
    pdf_path = os.path.join(tempfile.gettempdir(), pdf_filename)

    empresa = {
        "nombre": datos["empresa_nombre"],
        "rut": datos.get("empresa_rut", ""),
        "direccion": datos.get("empresa_direccion", "Calle"),
        "telefono": datos.get("empresa_telefono", "+56 9 7800 1874"),
        "logo_path": os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "templates", "assets", "img", "logo.png"
            )
        )
    }

    print(resultado["gratificacion"])

    generar_liquidacion_pdf(
        nombre=datos["empleado_nombre"],
        rut=datos["rut"],
        tipo_contrato=datos["tipo_contrato"],
        datos={
            'sueldo_base': resultado['sueldo_base'],
            'horas_extras': resultado.get('horas_extra', 0),
            'gratificacion': resultado.get('gratificacion'),
            'total_imponible': resultado.get('total_imponible', resultado['sueldo_base']),
            'afp': resultado['descuentos']['afp'],
            'salud': resultado['descuentos']['salud'],
            'afc': resultado['descuentos']['afc'],
            'total_descuentos': resultado['total_descuentos'],
            'liquido': resultado.get('sueldo_liquido', 0)
        },
        empresa=empresa,
        output_path=pdf_path
    )

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=pdf_filename
    )