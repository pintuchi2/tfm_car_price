import re

# def extraer_datos_tecnicos(tabla_datos_vehiculo):
#     # Paso 1: Campos fijos (0 a 6)
#     anyo = tabla_datos_vehiculo[0].get_text(strip=True)
#     kms = re.sub(r"[^\d]", "", tabla_datos_vehiculo[1].get_text(strip=True))
#     ciudad = tabla_datos_vehiculo[2].get_text(strip=True)
#     carroceria = tabla_datos_vehiculo[3].get_text(strip=True)
#     cambio = tabla_datos_vehiculo[4].get_text(strip=True).replace("Cambio", "").strip()
#     puertas = re.search(r"\d+", tabla_datos_vehiculo[5].get_text()).group()
#     plazas = re.search(r"\d+", tabla_datos_vehiculo[6].get_text()).group()

#     # Inicializar campos opcionales
#     cilindrada = potencia = color = emisiones = combustible = garantia = etiqueta = None

#     colores_posibles = ["negro", "blanco", "rojo", "gris", "azul", "verde", "marrón", "beige", "naranja", "amarillo", "plateado"]

#     for item in tabla_datos_vehiculo[7:]:
#         texto = item.get_text(strip=True)
#         texto_lower = texto.lower()

#         if "cc" in texto_lower:
#             cilindrada = re.search(r"\d+", texto).group()
#         elif "cv" in texto_lower:
#             potencia = re.search(r"\d+", texto).group()
#         elif any(color_pos in texto_lower for color_pos in colores_posibles) and "etiqueta" not in texto_lower:
#             color = texto
#         elif "gr/km" in texto_lower:
#             emisiones = re.search(r"\d+", texto).group()
#         elif any(x in texto_lower for x in ["diesel", "gasolina", "eléctrico", "híbrido", "hibrido enchufable"]):
#             combustible = texto.title()
#         elif "garantía" in texto_lower:
#             garantia = re.sub(r"garantía\s*", "", texto, flags=re.IGNORECASE).strip()
#         elif "etiqueta" in texto_lower:
#             etiqueta = re.sub(r"etiqueta\s*", "", texto, flags=re.IGNORECASE).strip()

#     return {
#         "anyo": anyo,
#         "kms": kms,
#         "ciudad": ciudad,
#         "carroceria": carroceria,
#         "cambio": cambio,
#         "puertas": puertas,
#         "plazas": plazas,
#         "cilindrada": cilindrada,
#         "potencia": potencia,
#         "color": color,
#         "emisiones": emisiones,
#         "combustible": combustible,
#         "garantia": garantia,
#         "etiqueta": etiqueta
#     }


def extraer_datos_tecnicos(tabla_datos_vehiculo):
    def extraer_numero(texto):
        match = re.search(r"\d+", texto)
        return match.group() if match else None

    # Campos fijos (con protección)
    anyo = tabla_datos_vehiculo[0].get_text(strip=True) if len(tabla_datos_vehiculo) > 0 else None
    kms = re.sub(r"[^\d]", "", tabla_datos_vehiculo[1].get_text(strip=True)) if len(tabla_datos_vehiculo) > 1 else None
    ciudad = tabla_datos_vehiculo[2].get_text(strip=True) if len(tabla_datos_vehiculo) > 2 else None
    carroceria = tabla_datos_vehiculo[3].get_text(strip=True) if len(tabla_datos_vehiculo) > 3 else None
    cambio = tabla_datos_vehiculo[4].get_text(strip=True).replace("Cambio", "").strip() if len(tabla_datos_vehiculo) > 4 else None
    puertas = extraer_numero(tabla_datos_vehiculo[5].get_text()) if len(tabla_datos_vehiculo) > 5 else None
    plazas = extraer_numero(tabla_datos_vehiculo[6].get_text()) if len(tabla_datos_vehiculo) > 6 else None

    # Inicializar campos opcionales
    cilindrada = potencia = color = emisiones = combustible = garantia = etiqueta = None

    colores_posibles = ["negro", "blanco", "rojo", "gris", "azul", "verde", "marrón", "beige", "naranja", "amarillo", "plateado"]

    for item in tabla_datos_vehiculo[7:]:
        texto = item.get_text(strip=True)
        texto_lower = texto.lower()

        if "cc" in texto_lower:
            cilindrada = extraer_numero(texto)
        elif "cv" in texto_lower:
            potencia = extraer_numero(texto)
        elif any(color_pos in texto_lower for color_pos in colores_posibles) and "etiqueta" not in texto_lower:
            color = texto
        elif "gr/km" in texto_lower:
            emisiones = extraer_numero(texto)
        elif any(x in texto_lower for x in ["diesel", "gasolina", "eléctrico", "híbrido", "hibrido enchufable"]):
            combustible = texto.title()
        elif "garantía" in texto_lower:
            garantia = re.sub(r"garantía\s*", "", texto, flags=re.IGNORECASE).strip()
        elif "etiqueta" in texto_lower:
            etiqueta = re.sub(r"etiqueta\s*", "", texto, flags=re.IGNORECASE).strip()

    return {
        "anyo": anyo,
        "kms": kms,
        "ciudad": ciudad,
        "carroceria": carroceria,
        "cambio": cambio,
        "puertas": puertas,
        "plazas": plazas,
        "cilindrada": cilindrada,
        "potencia": potencia,
        "color": color,
        "emisiones": emisiones,
        "combustible": combustible,
        "garantia": garantia,
        "etiqueta": etiqueta
    }
