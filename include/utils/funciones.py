import re
from unidecode import unidecode



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
            # Extraer solo el nombre del color en minúscula
            for color_pos in colores_posibles:
                if color_pos in texto_lower:
                    color = color_pos
                    break
        elif "gr/km" in texto_lower:
            emisiones = extraer_numero(texto)
        elif any(x in texto_lower for x in ["diesel", "diésel", "gasolina", "eléctrico", "híbrido", "hibrido"]):
            # Estandarizar el formato del combustible
            if "diesel" in texto_lower or "diésel" in texto_lower:
                combustible = "Diésel"
            elif "gasolina" in texto_lower:
                combustible = "Gasolina"
            elif "enchufable" in texto_lower or "plug-in" in texto_lower:
                combustible = "Híbrido enchufable"
            elif "eléctrico" in texto_lower:
                combustible = "Eléctrico"
            elif "híbrido" in texto_lower or "hibrido" in texto_lower:
                combustible = "Híbrido"
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



# Crear un diccionario de modelos estandarizados desde la base de datos
def cargar_modelos_estandarizados(cursor):
    cursor.execute("""
        SELECT marca, modelo 
        FROM TX_VEHICULOS_SEG_MANO 
        WHERE origen_anuncio = 'dataset kaggle' 
        GROUP BY marca, modelo
    """)
    
    modelos_por_marca = {}
    for marca, modelo in cursor.fetchall():
        if marca not in modelos_por_marca:
            modelos_por_marca[marca] = []
        modelos_por_marca[marca].append(modelo.lower().replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u"))
    
    return modelos_por_marca

# Función para encontrar el modelo estandarizado
def encontrar_modelo_estandarizado(marca, modelo_original, modelos_por_marca):
    marca_upper = marca.upper()
    modelo_tokens = set(modelo_original.lower().replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").split())
    
    if marca_upper not in modelos_por_marca:
        return modelo_original
    
    modelos = modelos_por_marca[marca_upper]
    mejor_modelo = modelo_original
    max_coincidencias = 0
    
    # Aquí devuelve el modelo en el que coincidan el mayor número de tokens del string
    for modelo_estandar in modelos:
        modelo_estandar_tokens = set(modelo_estandar.split())
        coincidencias = len(modelo_tokens.intersection(modelo_estandar_tokens))
        
        if coincidencias > max_coincidencias:
            max_coincidencias = coincidencias
            mejor_modelo = modelo_estandar
    
    return mejor_modelo