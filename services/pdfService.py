from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from datetime import datetime
import os

def generar_liquidacion_pdf(nombre, rut, tipo_contrato, datos, empresa, output_path):
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    # Logo de la empresa
    try:
        c.drawImage(empresa["logo_path"], 40, 750, width=80, height=80, preserveAspectRatio=True)
    except:
        pass

    # Datos de la empresa
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

    y_trabajador = 640

    # Fondo gris para datos del trabajador
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

    # Detalle de haberes
    y = y_trabajador - 70
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

    haberes = ["sueldo_base", "horas_extras", "gratificacion"]
    etiquetas_haberes = {
        "sueldo_base": "Sueldo Base",
        "horas_extras": "Horas Extras",
        "gratificacion": "Gratificación"
    }
    fila_alterna = True
    for key in haberes:
        if key in datos:
            if fila_alterna:
                c.setFillColor(colors.HexColor("#FAFAFA"))
                c.rect(40, y - 3, width - 80, 18, fill=True, stroke=False)
            c.setFillColor(colors.black)
            c.setFont("Helvetica", 10)
            c.drawString(50, y, etiquetas_haberes[key])
            c.drawRightString(width - 50, y, f"${datos[key]:,.0f}".replace(",", "."))
            y -= 18
            fila_alterna = not fila_alterna

    c.setStrokeColor(colors.HexColor("#333333"))
    c.setLineWidth(0.5)
    c.line(40, y + 15, width - 40, y + 15)
    y -= 5

    # Mostrar Total Haberes aunque venga como total_imponible si falta total_haberes
    y_fin_haberes = y + 3
    if "total_haberes" in datos:
        total_haberes_val = datos["total_haberes"]
    elif "total_imponible" in datos:
        total_haberes_val = datos["total_imponible"]
    else:
        total_haberes_val = None

    if total_haberes_val is not None:
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y, "Total Haberes")
        c.drawRightString(width - 50, y, f"${total_haberes_val:,.0f}".replace(",", "."))
        y_fin_haberes = y - 3

    c.setStrokeColor(colors.HexColor("#CCCCCC"))
    c.setLineWidth(1)
    altura_tabla_haberes = y_inicio_haberes - y_fin_haberes
    c.rect(40, y_fin_haberes, width - 80, altura_tabla_haberes, fill=False, stroke=True)

    # Detalle de descuentos
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
    descuentos = ["afp", "afc", "salud"]
    etiquetas_descuentos = {
        "afp": "AFP",
        "afc": "AFC",
        "salud": "FONASA / ISAPRE"
    }
    fila_alterna = True
    for key in descuentos:
        if key in datos:
            if fila_alterna:
                c.setFillColor(colors.HexColor("#FAFAFA"))
                c.rect(40, y - 3, width - 80, 18, fill=True, stroke=False)
            c.setFillColor(colors.black)
            c.setFont("Helvetica", 10)
            c.drawString(50, y, etiquetas_descuentos[key])
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

    # Total líquido
    y -= 70
    c.setFillColor(colors.HexColor("#4A4A4A"))
    c.setStrokeColor(colors.HexColor("#CCCCCC"))
    c.setLineWidth(1)
    c.rect(40, y, width - 80, 25, fill=True, stroke=True)

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50,y +10,"TOTAL A PAGAR")
    c.drawRightString(width - 50,y +10,"MONTO")
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

    # Pie - firma y fecha    # Pie con acuse de recibo y fecha.
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
