# services/pdfService.py - DISEÑO PROFESIONAL CON SUELDO BASE ORIGINAL Y PROPORCIONAL

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from datetime import datetime
import os


def generar_liquidacion_pdf(nombre, rut, tipo_contrato, datos, empresa, sueldo_base_original, dias_trabajados, output_path):
    """
    Genera PDF de liquidación con diseño profesional
    
    Parámetros:
    - nombre: Nombre del trabajador
    - rut: RUT del trabajador
    - tipo_contrato: Tipo de contrato (INDEFINIDO, PLAZO_FIJO)
    - datos: Dict con sueldo_base, horas_extra, gratificacion, afp, salud, afc, total_descuentos, liquido
    - empresa: Dict con nombre, rut, direccion, telefono, logo_path
    - sueldo_base_original: Sueldo base sin proporcionar
    - dias_trabajados: Días trabajados en el mes
    - output_path: Ruta donde guardar el PDF
    """
    
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    # ========== LOGO Y DATOS DE LA EMPRESA ==========
    try:
        c.drawImage(empresa["logo_path"], 40, 750, width=80, height=80, preserveAspectRatio=True)
    except:
        pass

    c.setFont("Helvetica-Bold", 14)
    c.drawString(140, 805, str(empresa["nombre"]))
    c.setFont("Helvetica", 9)
    c.drawString(140, 790, f"RUT: {str(empresa['rut'])}")
    c.drawString(140, 777, str(empresa["direccion"]))
    c.drawString(140, 764, "+56 9 " + str(empresa["telefono"]))

    # Línea separadora
    c.setStrokeColor(colors.HexColor("#000000"))
    c.setLineWidth(1)
    c.line(40, 735, width - 40, 735)

    # ========== DATOS DEL TRABAJADOR ==========
    y_trabajador = 640

    c.setFillColor(colors.HexColor("#F0F0F0"))
    c.setStrokeColor(colors.HexColor("#CCCCCC"))
    c.setLineWidth(1)
    c.rect(40, y_trabajador, width - 80, 75, fill=True, stroke=True)

    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y_trabajador + 60, "Datos del Trabajador")
    c.setFont("Helvetica", 10)
    c.drawString(50, y_trabajador + 42, f"Nombre: {nombre}")
    c.drawString(50, y_trabajador + 24, f"RUT: {rut}")
    c.drawString(50, y_trabajador + 6, f"Tipo de contrato: {tipo_contrato}")

    # ========== INFORMACIÓN DE PERÍODOS ==========
    """y = y_trabajador - 50
    c.setFont("Helvetica-Bold", 9)
    c.drawString(50, y, f"Período: {datetime.now().strftime('%B %Y').upper()}")
    c.drawString(50, y - 15, f"Días trabajados: {dias_trabajados}/30")
    
    if dias_trabajados < 30:
        c.drawString(50, y - 30, f"Sueldo Base (Original): ${sueldo_base_original:,.0f}".replace(",", "."))
        c.drawString(50, y - 45, f"Sueldo Base (Proporcional {dias_trabajados} días): ${datos['sueldo_base']:,.0f}".replace(",", "."))"""

    # ========== DETALLE DE HABERES ==========
    y = y_trabajador - 50
    c.setFillColor(colors.HexColor("#4A4A4A"))
    c.setStrokeColor(colors.HexColor("#CCCCCC"))
    c.setLineWidth(1)
    c.rect(40, y, width - 80, 25, fill=True, stroke=True)

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y + 10, "DETALLE DE HABERES")
    c.drawRightString(width - 50, y + 10, "MONTO")
    c.setFillColor(colors.black)

    y_inicio_haberes = y
    y -= 20

    haberes = [
        ("sueldo_base", "Sueldo Base Proporcional"),
        ("monto_horas_extra", "Horas Extras"),
        ("gratificacion", "Gratificación")
    ]
    
    fila_alterna = True
    for key, etiqueta in haberes:
        if key in datos and datos[key] > 0:
            if fila_alterna:
                c.setFillColor(colors.HexColor("#FAFAFA"))
                c.rect(40, y - 3, width - 80, 18, fill=True, stroke=False)
            c.setFillColor(colors.black)
            c.setFont("Helvetica", 10)
            c.drawString(50, y, etiqueta)
            c.drawRightString(width - 50, y, f"${datos[key]:,.0f}".replace(",", "."))
            y -= 18
            fila_alterna = not fila_alterna

    c.setStrokeColor(colors.HexColor("#333333"))
    c.setLineWidth(0.5)
    c.line(40, y + 15, width - 40, y + 15)
    y -= 5

    y_fin_haberes = y + 3
    if "total_imponible" in datos:
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y, "Total Haberes")
        c.drawRightString(width - 50, y, f"${datos['total_imponible']:,.0f}".replace(",", "."))
        y_fin_haberes = y - 3

    c.setStrokeColor(colors.HexColor("#CCCCCC"))
    c.setLineWidth(1)
    altura_tabla_haberes = y_inicio_haberes - y_fin_haberes
    c.rect(40, y_fin_haberes, width - 80, altura_tabla_haberes, fill=False, stroke=True)

    # ========== DETALLE DE DESCUENTOS ==========
    y -= 70
    c.setFillColor(colors.HexColor("#4A4A4A"))
    c.setStrokeColor(colors.HexColor("#CCCCCC"))
    c.setLineWidth(1)
    c.rect(40, y, width - 80, 25, fill=True, stroke=True)

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y + 10, "DETALLE DE DESCUENTOS")
    c.drawRightString(width - 50, y + 10, "MONTO")
    c.setFillColor(colors.black)

    y_inicio_descuentos = y
    y -= 20
    
    descuentos = [
        ("afp", "AFP"),
        ("salud", "FONASA / ISAPRE"),
        ("afc", "AFC")
    ]
    
    fila_alterna = True
    for key, etiqueta in descuentos:
        if key in datos and datos[key] > 0:
            if fila_alterna:
                c.setFillColor(colors.HexColor("#FAFAFA"))
                c.rect(40, y - 3, width - 80, 18, fill=True, stroke=False)
            c.setFillColor(colors.black)
            c.setFont("Helvetica", 10)
            c.drawString(50, y, etiqueta)
            c.drawRightString(width - 50, y, f"$ -{datos[key]:,.0f}".replace(",", "."))
            y -= 18
            fila_alterna = not fila_alterna

    c.setStrokeColor(colors.HexColor("#333333"))
    c.setLineWidth(0.5)
    c.line(40, y + 15, width - 40, y + 15)
    y -= 5

    y_fin_descuentos = y + 3
    if "total_descuentos" in datos:
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y, "Total Descuentos")
        c.drawRightString(width - 50, y, f"$ -{datos['total_descuentos']:,.0f}".replace(",", "."))
        y_fin_descuentos = y - 3

    c.setStrokeColor(colors.HexColor("#CCCCCC"))
    c.setLineWidth(1)
    altura_tabla_descuentos = y_inicio_descuentos - y_fin_descuentos
    c.rect(40, y_fin_descuentos, width - 80, altura_tabla_descuentos, fill=False, stroke=True)

    # ========== TOTAL A PAGAR ==========
    y -= 70
    c.setFillColor(colors.HexColor("#4A4A4A"))
    c.setStrokeColor(colors.HexColor("#CCCCCC"))
    c.setLineWidth(1)
    c.rect(40, y, width - 80, 25, fill=True, stroke=True)

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y + 10, "TOTAL A PAGAR")
    c.drawRightString(width - 50, y + 10, "MONTO")
    c.setFillColor(colors.black)
    
    y_inicio_total = y
    y -= 20
    y_fin_total = y + 3
    
    if "liquido" in datos:
        c.setFillColor(colors.HexColor("#FAFAFA"))
        c.rect(40, y - 3, width - 80, 18, fill=True, stroke=False)
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y, "Líquido a Pagar")
        c.drawRightString(width - 50, y, f"${datos['liquido']:,.0f}".replace(",", "."))
        y_fin_total = y - 3
    
    c.setStrokeColor(colors.HexColor("#CCCCCC"))
    c.setLineWidth(1)
    altura_tabla_total = y_inicio_total - y_fin_total
    c.rect(40, y_fin_total, width - 80, altura_tabla_total, fill=False, stroke=True)

    # ========== PIE - FIRMA Y FECHA ==========
    margen_inferior = 40
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(40, margen_inferior + 60, "ACUSO DE RECIBO")
    c.setFont("Helvetica", 9)
    c.drawString(40, margen_inferior + 40, "Declaro haber recibido conforme la liquidación de sueldo descrita en este documento.")
    c.setLineWidth(0.5)
    c.line(40, margen_inferior + 20, 250, margen_inferior + 20)
    c.setFont("Helvetica", 8)
    c.drawString(40, margen_inferior + 5, "Firma del Trabajador")
    c.drawString(485, margen_inferior + 5, f"Fecha: {datetime.now().strftime('%d/%m/%Y')}")
    
    c.save()