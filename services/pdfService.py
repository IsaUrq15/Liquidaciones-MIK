def generar_liquidacion_pdf(nombre, rut, cargo, datos, empresa, output_path):
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    from reportlab.lib import colors

    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    # Logo de la empresa
    c.drawImage(empresa["logo_path"], 40, 750, width=80, height=80, preserveAspectRatio=True)
    
    # Datos de la empresa
    c.setFont("Helvetica-Bold", 14)
    c.drawString(140, 805, empresa["nombre"])
    c.setFont("Helvetica", 9)
    c.drawString(140, 790, f"RUT: {empresa['rut']}")
    c.drawString(140, 777, empresa["direccion"])
    c.drawString(140, 764, empresa["telefono"])
    
    # Línea separadora entre encabezado y contenido (debajo del logo/datos de empresa)
    c.setStrokeColor(colors.HexColor("#000000"))
    c.setLineWidth(1)
    c.line(40, 735, width - 40, 735)
    
    # 50 píxeles de separación desde la línea (735 - 50 = 685, menos 75 de altura = 610)
    y_trabajador = 640
    
    # Fondo gris para datos del trabajador
    c.setFillColor(colors.HexColor("#F0F0F0"))
    c.setStrokeColor(colors.HexColor("#CCCCCC"))
    c.setLineWidth(1)
    c.rect(40, y_trabajador, width - 80, 75, fill=True, stroke=True)
    
    # Restablecer color negro para el texto
    c.setFillColor(colors.black)
    
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y_trabajador + 60, "Datos del Trabajador")
    
    c.setFont("Helvetica", 10)
    c.drawString(50, y_trabajador + 42, f"Nombre: {nombre}")
    c.drawString(50, y_trabajador + 24, f"RUT: {rut}")
    c.drawString(50, y_trabajador + 6, f"Cargo: {cargo}")

    # TABLA 1: DETALLE DE HABERES

    y = y_trabajador - 70  # 70 píxeles de separación desde datos del trabajador
    
    # Encabezado de HABERES
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
    
    # Items de haberes
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
    
    # Línea separadora
    c.setStrokeColor(colors.HexColor("#333333"))
    c.setLineWidth(0.5)
    c.line(40, y + 15, width - 40, y + 15)
    y -= 5
    
    # Total Haberes
    if "total_haberes" in datos:
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y, "Total Haberes")
        c.drawRightString(width - 50, y, f"${datos['total_haberes']:,.0f}".replace(",", "."))
        y_fin_haberes = y - 3
    
    # Borde completo de la tabla de haberes
    c.setStrokeColor(colors.HexColor("#CCCCCC"))
    c.setLineWidth(1)
    altura_tabla_haberes = y_inicio_haberes - y_fin_haberes
    c.rect(40, y_fin_haberes, width - 80, altura_tabla_haberes, fill=False, stroke=True)
    
    y -= 70  # Espacio de 70 píxeles antes de la siguiente tabla

    # TABLA 2: DETALLE DE DESCUENTOS
    
    # Encabezado de DESCUENTOS
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
    
    # Items de descuentos
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
    
    # Línea separadora
    c.setStrokeColor(colors.HexColor("#333333"))
    c.setLineWidth(0.5)
    c.line(40, y + 15, width - 40, y + 15)
    y -= 5
    
    # Total Descuentos
    if "total_descuentos" in datos:
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y, "Total Descuentos")
        c.drawRightString(width - 50, y, f"$ -{datos['total_descuentos']:,.0f}".replace(",", "."))
        y_fin_descuentos = y - 3
    
    # Borde completo de la tabla de descuentos
    c.setStrokeColor(colors.HexColor("#CCCCCC"))
    c.setLineWidth(1)
    altura_tabla_descuentos = y_inicio_descuentos - y_fin_descuentos
    c.rect(40, y_fin_descuentos, width - 80, altura_tabla_descuentos, fill=False, stroke=True)
    
    y -= 70  # Espacio de 70 píxeles antes de la siguiente tabla

    # TABLA 3: TOTAL LIQUIDO
    
    # Encabezado de TOTAL LIQUIDO
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
    
    # Líquido a Pagar
    if "liquido" in datos:
        c.setFillColor(colors.HexColor("#FAFAFA"))
        c.rect(40, y - 3, width - 80, 18, fill=True, stroke=False)
        c.setFillColor(colors.black)
        
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y, "Líquido a Pagar")
        c.drawRightString(width - 50, y, f"${datos['liquido']:,.0f}".replace(",", "."))
        y_fin_total = y - 3
    
    # Borde completo de la tabla de total a pagar
    c.setStrokeColor(colors.HexColor("#CCCCCC"))
    c.setLineWidth(1)
    altura_tabla_total = y_inicio_total - y_fin_total
    c.rect(40, y_fin_total, width - 80, altura_tabla_total, fill=False, stroke=True)

    # PIE DE PÁGINA - FIRMA (AL FINAL DE LA PÁGINA)

    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(40, 80, "ACUSO DE RECIBO")
    
    c.setFont("Helvetica", 9)
    c.drawString(40, 60, "Declaro haber recibido conforme la liquidación de sueldo descrita en este documento.")
    
    # Línea de firma
    c.setLineWidth(0.5)
    c.line(40, 30, 250, 30)
    c.setFont("Helvetica", 8)
    c.drawString(40, 18, "Firma del Trabajador")
    
    # Fecha
    c.line(350, 30, 520, 30)
    c.drawString(350, 18, "Fecha: ____/____/______")

    # GUARDAR DOCUMENTO

    c.save()