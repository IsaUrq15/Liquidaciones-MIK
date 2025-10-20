def generar_liquidacion_pdf(nombre, rut, cargo, datos, empresa, output_path):
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas

    c = canvas.Canvas(output_path, pagesize=A4)

    # --- Logo ---
    c.drawImage(empresa["logo_path"], 40, 750, width=80, height=80, preserveAspectRatio=True)

    # --- Datos empresa ---
    c.setFont("Helvetica-Bold", 12)
    c.drawString(140, 800, empresa["nombre"])
    c.setFont("Helvetica", 10)
    c.drawString(140, 785, f"RUT: {empresa['rut']}")
    c.drawString(140, 770, empresa["direccion"])
    c.drawString(140, 755, empresa["telefono"])

    # --- Datos trabajador ---
    c.setFont("Helvetica-Bold", 11)
    c.drawString(40, 710, "Datos del Trabajador")
    c.setFont("Helvetica", 10)
    c.drawString(40, 695, f"Nombre: {nombre}")
    c.drawString(40, 680, f"RUT: {rut}")
    c.drawString(40, 665, f"Cargo: {cargo}")

    # --- Detalle de haberes y descuentos ---
    c.setFont("Helvetica-Bold", 11)
    c.drawString(40, 630, "Detalle de Haberes y Descuentos")

    # Diccionario de nombres legibles
    etiquetas = {
        "sueldo_base": "Sueldo Base",
        "horas_extras": "Horas Extras",
        "gratificacion": "Gratificación",
        "total_haberes": "Total Haberes",
        "afp": "AFP",
        "afc": "AFC",
        "salud": "FONASA / ISAPRE",
        "total_descuentos": "Total Descuentos",
        "liquido": "Liquido a Pagar"
    }

    y = 610
    for key, value in datos.items():
        nombre_legible = etiquetas.get(key, key)  # si no existe, usa la clave original
        c.setFont("Helvetica-Bold", 10)
        c.drawString(60, y, f"{nombre_legible}:")
        c.setFont("Helvetica", 10)
        c.drawRightString(300, y, f"${value:,.0f}".replace(",", "."))
        y -= 15


    # --- Pie de firma ---
    c.setFont("Helvetica-Bold", 11)
    c.drawString(40, 150, "Acuso de recibo:")
    c.setFont("Helvetica", 10)
    c.drawString(40, 130, "El trabajador(a) _________________________      Fecha: ____/____/______")

    c.save()