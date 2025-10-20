def calcular_liquidacion(sueldo_base: float, horas_extras: float, inm: float = 529000) -> dict:

    # --- Gratificación legal (25% del sueldo, con tope) ---
    tope_gratificacion = (4.75 * inm) / 12
    gratificacion = min(sueldo_base * 0.25, tope_gratificacion)

    total_haberes = sueldo_base + horas_extras + gratificacion

    afp = sueldo_base * 0.10       # 10%
    afc = sueldo_base * 0.006      # 0.6%
    salud = sueldo_base * 0.07     # 7%

    horas_extras = (((((sueldo_base / 30) * 7) / 44) * 1.5) * horas_extras)

    total_descuentos = afp + afc + salud
    liquido = total_haberes - total_descuentos

    return {
        "sueldo_base": sueldo_base,
        "horas_extras": horas_extras,
        "gratificacion": gratificacion,
        "total_haberes": total_haberes,
        "afp": afp,
        "afc": afc,
        "salud": salud,
        "total_descuentos": total_descuentos,
        "liquido": liquido
    }