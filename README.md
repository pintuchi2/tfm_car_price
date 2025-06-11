# 🚗 Web Scraper de Vehículos - Coches.net

Este proyecto realiza un scraping automatizado del portal [coches.net](https://www.coches.net/segunda-mano/) para recopilar anuncios de vehículos de segunda mano. La información se guarda en una base de datos SQLite local.


## Archivos y carpetas principales:

### dags:

Esta carpeta contiene el script `dag_coches_net_scraping.py` de orquestación del web scraping que permite la ejecución programada del mismo en Airflow.

### notebooks:

Esta carpeta contiene 6 jupyter notebooks con el desarrollo del código del tfm:

- `ml_car_price_prediction.ipynb`: Es el notebook principal, que contiene el EDA y desarrollo del modelo de machine learning implementado para la predicción del precio de los vehículos.

- `undetected_scraper.ipynb`: Este notebook contiene el script que realiza el web scraping de [coches.net](https://www.coches.net) y guarda los registros en la tabla `TX_VEHICULOS_SEG_MANO` de la base de datos que hemos creado. Este script se moverá a un archivo `.py` y se invocará con el dag de Airflow pero falta impementarlo.

- `kaggle_dataset_cleaning.ipynb`: Notebook que contiene transformaciones y limpieza de datos para combinar los datos obtenidos mediante web scraping con datos con otro origen: un dataset de Kaggle de vehículos de 2a mano obtenidos también mediante web scraping.

- `kaggle_dataset_cleaning_nuevas_marcas.ipynb`: Contiene las mismas transformaciones que el notebook anterior pero para 4 nuevas marcas de vehículos incorporadas posteriormente.

- `pruebas_scraping.ipynb`: Notebook que contiene pruebas para el desarrollo del script de scrapeo que se utiliza en el archivo `undetected_scraper.ipynb`.

- `transformaciones_webscraping.ipynb`: Notebook que contiene transformaciones y limpieza de datos de los datos scrapeados de [coches.net](https://www.coches.net). No tiene relevancia.

### streamlit:

- `streamlit_app.py`: Aplicación web desarrollada con Streamlit que permite predecir el precio de un vehículo en base a las características que el usuario introduce (marca, modelo, año, kilómetros, combustible, etc.) utilizando el modelo generado en el notebook `ml_car_price_prediction.ipynb`.

- utils: Carpeta que contiene las transformaciones y el modelo utilizados para realizar la predicción del precio del vehículo.

### include:

- utils: Carpeta que contiene:

    - Un archivo `funciones.py` con funciones reutilizables por el webscraper utilizadas para realizar la predicción del precio del vehículo.

    - El script `coches_net_scraper.py`, que es el script ejecutado desde el DAG de Airflow que realiza el web scraping programado.

    - Archivos .pkl que contienen las transformaciones finales utilizadas para realizar la predicción del precio del vehículo.

- model: Carpeta que contiene el modelo final utilizado para realizar la predicción del precio del vehículo.

- data: Datos del dataset de Kaggle utilizado como origen de datos (además de los scrapeados) y de pruebas y trasnformaciones llevadas a cabo en los notebooks.

- db_*.db: Estos archivos son la base de datos de tipo SQLite que utilizamos para guardar todos los registros y su Backup.

### `requirements.txt`
Lista de dependencias necesarias para ejecutar el proyecto.


## Otros archivos:

Además, existen otras carpetas y archivos que permiten la compatibilidad y reproducibilidad del proyecto utilizando Docker y Astro para la ejecución automática del trabajo de Airflow que realiza el web scraping. Algunos de estos archivos son el Dockerfile, chromedriver, etc.

Para desplegar el proyecto en local:
===========================

1. Instalar Astro y Docker Desktop y ejecutar el comando 'astro dev init'.

2. Iniciar Airflow en local utilizando el comando 'astro dev start'

Este comando creará 4 contenedores de Docker en tu ordenador, uno para cada uno de estos componentes:

- Postgres: La base de datos de metadatos de Airflow
- Webserver: El componente de Airflow responsable de mostrar la interfaz de usuario (UI) de Airflow
- Scheduler: El componente de Airflow responsable de monitorear y activar tareas
- Triggerer: El componente de Airflow responsable de activar tareas diferidas

3. Verificar que se han creado cada uno de estos 4 contenedores de Docker con el comando 'docker ps'.

Nota: Ejecutar astro dev start iniciará tu proyecto con el servidor web de Airflow expuesto en el puerto 8080 y Postgres expuesto en el puerto 5432. Si ya tienes asignado alguno de esos puertos, puedes [detener tus contenedores Docker existentes o cambiar el puerto](https://www.astronomer.io/docs/astro/cli/troubleshoot-locally#ports-are-not-available-for-my-local-airflow-webserver).

4. Accede a la interfaz de usuario de Airflow de tu proyecto local. Para ello, abre http://localhost:8080/ e inicia sesión con “admin” tanto en Nombre de usuario como en Contraseña.