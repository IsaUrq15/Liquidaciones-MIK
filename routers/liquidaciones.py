from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from dto.liquidacion import LiquidacionCreate
from utils.liquidacionService import calcular_liquidacion
from services.pdfService import generar_liquidacion_pdf
import os
import tempfile

router = APIRouter(prefix="/liquidaciones", tags=["liquidacion"])

@router.post("/generar", response_class=FileResponse)
def crear_liquidacion(liquidacion: LiquidacionCreate):
    try:
        # Calcular datos de la liquidación
        datos = calcular_liquidacion(
            liquidacion.sueldo_base,
            liquidacion.horas_extras
        )

        # Datos de la empresa
        empresa = {
            "nombre": "Finantel Group SpA",
            "rut": "77.123.456-7",
            "direccion": "Av. Los Leones 1234, Santiago",
            "telefono": "+56 9 8765 4321",
            "logo_path": os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    "..",  # sube de routers/ a DesarolloWeb2/
                    "templates", "assets", "img", "logo.png"
                )
            )
        }

        # Verificar que el logo exista
        if not os.path.exists(empresa["logo_path"]):
            raise HTTPException(status_code=404, detail=f"Logo no encontrado en {empresa['logo_path']}")

        # Generar PDF (en archivo temporal)
        pdf_path = os.path.join(tempfile.gettempdir(), f"liquidacion_{liquidacion.nombre.replace(' ', '_')}.pdf")
        generar_liquidacion_pdf(
            nombre=liquidacion.nombre,
            rut=liquidacion.rut,
            cargo=liquidacion.cargo,
            datos=datos,
            empresa=empresa,
            output_path=pdf_path
        )

        # Devolver PDF generado
        return FileResponse(
            path=pdf_path,
            media_type="application/pdf",
            filename=f"liquidacion_{liquidacion.nombre.replace(' ', '_')}.pdf"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))