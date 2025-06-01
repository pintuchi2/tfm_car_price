import time
from datetime import datetime, timedelta
import random
import sqlite3
import sys
import os
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup as bs


sys.path.append(os.path.abspath("../../")) 
from include.utils.funciones import *

# Conexión a la BBDD:
con = sqlite3.connect("./include/db_vehiculos.db")
cursor = con.cursor()


# Cargar modelos estandarizados:
modelos_estandarizados = cargar_modelos_estandarizados(cursor)
print(f"📚 Cargados {sum(len(modelos) for modelos in modelos_estandarizados.values())} modelos estandarizados de {len(modelos_estandarizados)} marcas")

# User agents aleatorios:
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:99.0) Gecko/20100101 Firefox/99.0",
]

options = uc.ChromeOptions()
options.binary_location = "/usr/bin/chromium"
# options.binary_location = "/usr/local/bin/chrome"

selected_ua = random.choice(USER_AGENTS)
# options.add_argument(f"user-agent={selected_ua}")
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_argument("--headless")  # opcional

# Config para Docker:
options.add_argument(f"user-agent={selected_ua}")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--headless=new")  # nuevo modo headless más estable
options.add_argument("--window-size=1920,1080")


# Inicializar navegador:
driver = uc.Chrome(options=options,
                #    driver_executable_path="/usr/bin/chromedriver",)
                   driver_executable_path="/opt/chromedriver/chromedriver",
                   patcher=False,
                   version_main=137,
                   use_subprocess=True)

# Marcas de coche scrapeadas:
lista_marcas = ['BMW', 'VOLKSWAGEN', 'MERCEDES-BENZ', 'AUDI', 'PEUGEOT', 
                'FORD', 'RENAULT', 'OPEL', 'CITROEN', 'SEAT']

# Mantener un registro de IDs procesados durante esta ejecución:
ids_procesados_sesion = set()

# Lista de IDs en la BBDD:
cursor.execute("SELECT PK_ANUNCIO_ID FROM TX_VEHICULOS_SEG_MANO")
ids_existentes = {fila[0] for fila in cursor.fetchall()}

pagina = 1
max_paginas = 25  # Número de páginas a scrapear

while pagina < max_paginas:
    print(f"\n🔄 Procesando página {pagina}...")
    
    # URL para todas las marcas configuradas:
    url_todas_marcas = f'https://www.coches.net/segunda-mano/?MakeIds%5B0%5D=4&MakeIds%5B1%5D=7&MakeIds%5B2%5D=11&MakeIds%5B3%5D=15&MakeIds%5B4%5D=28&MakeIds%5B5%5D=32&MakeIds%5B6%5D=33&MakeIds%5B7%5D=35&MakeIds%5B8%5D=39&MakeIds%5B9%5D=47&ModelIds%5B0%5D=0&ModelIds%5B1%5D=0&ModelIds%5B2%5D=0&ModelIds%5B3%5D=0&ModelIds%5B4%5D=0&ModelIds%5B5%5D=0&ModelIds%5B6%5D=0&ModelIds%5B7%5D=0&ModelIds%5B8%5D=0&ModelIds%5B9%5D=0&Versions%5B0%5D=&Versions%5B1%5D=&Versions%5B2%5D=&Versions%5B3%5D=&Versions%5B4%5D=&Versions%5B5%5D=&Versions%5B6%5D=&Versions%5B7%5D=&Versions%5B8%5D=&Versions%5B9%5D=&pg={pagina}'
    
    # Cargar la página de listado
    driver.get(url_todas_marcas)
    time.sleep(random.uniform(4, 6))

    # Aceptar cookies si aparecen (solo en la primera página):
    if pagina == 1:
        try:
            cookies_button = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/div/div[3]/button[3]")
            cookies_button.click()
            print("✅ Cookies aceptadas")
            time.sleep(1)
        except Exception as e:
            print(f"ℹ️ No fue necesario aceptar cookies: {e}")

    # Obtener página:
    soup = bs(driver.page_source, "lxml")
    
    # Extraer IDs de vehículos de la página actual:
    vehiculos_elementos = soup.select("div[data-ad-id]")
    lista_id_vehiculos = [div["data-ad-id"] for div in vehiculos_elementos]
    
    if not lista_id_vehiculos:
        print("✅ No hay más anuncios en esta página. Fin del scraping.")
        break
    
    print(f"📋 Encontrados {len(lista_id_vehiculos)} vehículos en la página {pagina}")
    
    # Procesar cada vehículo de la página:
    for i, id_vehiculo in enumerate(lista_id_vehiculos, 1):
        # Verificar si ya hemos procesado este ID en esta sesión o existe en BD:
        if id_vehiculo in ids_procesados_sesion:
            print(f"⏭️ ID {id_vehiculo} ya procesado en esta sesión, saltando")
            continue
            
        if id_vehiculo in ids_existentes:
            print(f"⏭️ ID {id_vehiculo} ya existe en la base de datos, saltando")
            continue
        
        print(f"\n🚗 Procesando vehículo {i}/{len(lista_id_vehiculos)} - ID: {id_vehiculo}")
        
        # Marcar como procesado antes de comenzar:
        ids_procesados_sesion.add(id_vehiculo)
        
        try:
            # Buscar el elemento correcto para hacer clic:
            try:

                # Encontrar el elemento por XPath fijo:
                # print(f"Procesando vehículo {i}/{len(lista_id_vehiculos)} - ID: {id_vehiculo}")

                # xpath_anuncio = f"/html/body/div[2]/div/div[2]/div[1]/div[1]/main/div[4]/section/div[1]/div[{i}]/div/div"
                # anuncio_vehiculo = driver.find_element(By.XPATH, xpath_anuncio)
                # anuncio_vehiculo.click()
                # time.sleep(random.uniform(5, 15))

                # Encontrar el elemento por data-ad-id:
                selector = f"div[data-ad-id='{id_vehiculo}']"
                anuncio_vehiculo = driver.find_element(By.CSS_SELECTOR, selector)
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", anuncio_vehiculo)
                time.sleep(random.uniform(1, 2))
                anuncio_vehiculo.click()
            except Exception as e:
                print(f"❌ No se pudo hacer clic en el anuncio: {e}")

                # Volver a cargar la página y continuar con el siguiente vehículo:
                driver.get(url_todas_marcas)
                time.sleep(random.uniform(5, 8))
                continue

            # Esperar a que se cargue la página de detalle:
            time.sleep(random.uniform(8, 12))

            # Verificar y manejar múltiples pestañas:
            main_window = driver.current_window_handle
            if len(driver.window_handles) > 1:
                for handle in driver.window_handles:
                    if handle != main_window:
                        driver.switch_to.window(handle)
                        print("🔴 Pestaña externa detectada. Cerrando...")
                        driver.close()
                driver.switch_to.window(main_window)

            # Simular movimiento de ratón con límites seguros:
            try:
                # Obtener dimensiones del viewport (área visible)
                viewport_width = driver.execute_script("return window.innerWidth;")
                viewport_height = driver.execute_script("return window.innerHeight;")
                
                # Calcular coordenadas seguras (80% del viewport para evitar bordes)
                safe_width = int(viewport_width * 0.8)
                safe_height = int(viewport_height * 0.8)
                
                # Mover a una posición aleatoria dentro del área segura
                x_coord = random.randint(100, max(200, safe_width))
                y_coord = random.randint(100, max(200, safe_height))
                
                # Usar JavaScript para mover el mouse (más fiable que ActionChains)
                driver.execute_script(f"""
                    var event = new MouseEvent('mousemove', {{
                        'view': window,
                        'bubbles': true,
                        'cancelable': true,
                        'clientX': {x_coord},
                        'clientY': {y_coord}
                    }});
                    document.dispatchEvent(event);
                """)
                
                print(f"🖱️ Movimiento del ratón simulado a ({x_coord}, {y_coord})")
                time.sleep(random.uniform(1, 3))
            except Exception as e:
                print(f"⚠️ No se pudo simular movimiento del ratón: {e}")
                # Continuar aunque no se pueda simular el movimiento

            # Capturar URL actual y contenido de la página
            url_vehiculo = driver.current_url
            soup_vehiculo = bs(driver.page_source, "lxml")

            # Extraer título y separar marca/modelo
            title_element = soup_vehiculo.select_one('h1.mt-TitleBasic-title')
            if not title_element:
                raise Exception("No se encontró el título del vehículo")

            palabras = title_element.get_text(strip=True).split()
            marca_vehiculo = palabras[0]
            modelo_vehiculo_original = " ".join(palabras[1:])
            
            # Aplicar estandarización del modelo usando el diccionario de referencia
            modelo_vehiculo = encontrar_modelo_estandarizado(
                marca_vehiculo, 
                modelo_vehiculo_original, 
                modelos_estandarizados
            )
            
            if modelo_vehiculo != modelo_vehiculo_original:
                print(f"📝 Modelo estandarizado: {modelo_vehiculo_original} -> {modelo_vehiculo}")
            else:
                print(f"📝 Analizando: {marca_vehiculo} {modelo_vehiculo}")

            # Extraer precio
            precio = None
            string_precio = soup_vehiculo.find("p", class_="mt-CardAdPrice-cashAmount")
            if string_precio:
                texto_precio = string_precio.text.strip().replace('.', '').replace('€', '').strip()
                try:
                    precio = float(texto_precio)
                except ValueError:
                    print(f"⚠️ No se pudo convertir el precio: {texto_precio}")

            # Extraer datos técnicos
            tabla_datos_vehiculo = soup_vehiculo.select('ul.mt-PanelAdDetails-data li.mt-PanelAdDetails-dataItem')
            dicc = extraer_datos_tecnicos(tabla_datos_vehiculo)

            # Procesar fecha de publicación
            hoy = datetime.now()
            fecha_actual = hoy.strftime("%d/%m")
            string_fecha_publicacion = soup_vehiculo.find("p", class_="mt-PanelAdInfo-published")
            fecha_final_publicacion = None
            anyomes_publicacion = None

            if string_fecha_publicacion:
                texto = string_fecha_publicacion.text.strip().lower()

                if "hace" in texto or "hoy" in texto or "ahora" in texto:
                    fecha_final_publicacion = datetime.now().date()
                elif "ayer" in texto:
                    fecha_final_publicacion = (datetime.now() - timedelta(days=1)).date()
                else:
                    try:
                        # Ejemplo: "Publicado: 12/03, hace 3 días"
                        fecha_str = texto.split(",")[0].replace("publicado: ", "").strip()[0:5]
                        fecha_publicacion_dt = datetime.strptime(fecha_str, "%d/%m")
                        fecha_actual_dt = datetime.strptime(fecha_actual, "%d/%m")

                        # Ajuste de año si es diciembre vs enero
                        anyo = hoy.year - 1 if fecha_publicacion_dt > fecha_actual_dt else hoy.year
                        fecha_final_publicacion = datetime.strptime(f"{fecha_str}/{anyo}", "%d/%m/%Y").date()
                    except Exception as e:
                        print(f"⚠️ No se pudo interpretar la fecha: {texto} - {e}")
                        fecha_final_publicacion = None

                if fecha_final_publicacion:
                    anyomes_publicacion = int(f"{fecha_final_publicacion.year}{fecha_final_publicacion.month:02d}")

            # Preparar consulta SQL e insertar datos
            consulta = """
                INSERT OR IGNORE INTO TX_VEHICULOS_SEG_MANO (
                    pk_anuncio_id, marca, modelo, precio, combustible, anyo_vehiculo,
                    kilometraje, potencia, num_puertas, num_plazas, tipo_cambio,
                    tipo_vehiculo, cilindrada_motor, color, provincia, etiqueta_eco,
                    origen_anuncio, fecha_publicacion, anyomes_publicacion, url
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

            valores = (
                id_vehiculo,
                marca_vehiculo,
                modelo_vehiculo,
                precio,
                dicc.get("combustible"),
                int(dicc.get("anyo")) if dicc.get("anyo") else None,
                int(dicc.get("kms")) if dicc.get("kms") else None,
                int(dicc.get("potencia")) if dicc.get("potencia") else None,
                int(dicc.get("puertas")) if dicc.get("puertas") else None,
                int(dicc.get("plazas")) if dicc.get("plazas") else None,
                dicc.get("cambio"),
                dicc.get("carroceria"),
                int(dicc.get("cilindrada")) if dicc.get("cilindrada") else None,
                dicc.get("color"),
                dicc.get("ciudad"),
                dicc.get("etiqueta"),
                "WebScraping",
                fecha_final_publicacion,
                anyomes_publicacion,
                url_vehiculo
            )

            cursor.execute(consulta, valores)
            con.commit()
            print(f"✅ Insertado vehículo ID {id_vehiculo} en la base de datos")

            # Pausa antes de volver atrás
            time.sleep(random.uniform(3, 5))
            
            # Volver a la página de listado y esperar a que cargue
            driver.back()
            time.sleep(random.uniform(5, 8))
            
            # Verificar que estamos en la página correcta después de volver atrás
            actual_url = driver.current_url
            if str(pagina) not in actual_url or "segunda-mano" not in actual_url:
                print("⚠️ Después de ir hacia atrás no estamos en la página esperada. Recargando...")
                driver.get(url_todas_marcas)
                time.sleep(random.uniform(5, 8))
            
            # Pausa larga cada 5 u 8 vehículos para simular comportamiento humano
            if (i % 5 == 0) or (i % 8 == 0):
                pausa = random.uniform(20, 30)
                print(f"⏸️ Pausa larga de {pausa:.1f} segundos simulando descanso del usuario...")
                time.sleep(pausa)

        except Exception as e:
            print(f"❌ Error al procesar ID {id_vehiculo}: {e}")
            # Intentar volver a la página de listado en caso de error
            try:
                driver.get(url_todas_marcas)
                time.sleep(random.uniform(5, 8))
            except:
                print("⚠️ Error al intentar recargar la página de listado")
                pass

    print(f"✅ Finalizada página {pagina}")
    pagina += 1

# Añadir stats finales
print(f"\n📊 Estadísticas finales:")
print(f"- Páginas procesadas: {pagina-1}")
print(f"- IDs procesados en esta sesión: {len(ids_procesados_sesion)}")

# Cierre final
driver.quit()
con.close()
print("🏁 Proceso finalizado correctamente")