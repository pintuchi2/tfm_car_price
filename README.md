# 🚗 Web Scraper de Vehículos - Coches.net

Este proyecto realiza un scraping automatizado del portal [coches.net](https://www.coches.net) para recopilar anuncios de vehículos de segunda mano. La información se guarda en una base de datos SQLite local.


## Archivos y carpetas principales:

### dags:

Esta carpeta contendrá el script de orquestación del WebScraping y entrenamiento del modelo, para realizar la automatización. Por el momento aún no está listo.

### notebooks:

Esta carpeta contiene 5 jupyter notebooks con el desarrollo del código del tfm:

- `ml_car_price_prediction.ipynb`: Es el notebook principal, que contiene el EDA y desarrollo del modelo de machine learning implementado para la predicción del precio de los vehículos.

- `undetected_scraper.ipynb`: Este notebook contiene el script que realiza el WebScraping de [coches.net](https://www.coches.net) y guarda los registros en la tabla `TX_VEHICULOS_SEG_MANO` de la base de datos que hemos creado. Este script se moverá a un archivo `.py` y se invocará con el dag de Airflow pero falta impementarlo.

- `kaggle_dataset_cleaning.ipynb`: Notebook que contiene transformaciones y limpieza de datos para combinar los datos obtenidos mediante WebScraping con datos con otro origen: un dataset de Kaggle de vehículos de 2a mano obtenidos también mediante WebScraping.

- `pruebas_scraping.ipynb`: Notebook que contiene pruebas para el desarrollo del script de scrapeo que se utiliza en el archivo `undetected_scraper.ipynb`.

- `transformaciones_webscraping.ipynb`: Notebook que contiene transformaciones y limpieza de datos de los datos scrapeados de [coches.net](https://www.coches.net). No tiene relevancia.

### streamlit:

- `streamlit_app.py`: Aplicación web desarrollada con Streamlit que permite predecir el precio de un vehículo en base a las características que el usuario introduce (marca, modelo, año, kilómetros, combustible, etc.) utilizando el modelo generado en el notebook `ml_car_price_prediction.ipynb`.

- utils: Carpeta que contiene las transformaciones y el modelo utilizados para realizar la predicción del precio del vehículo.

### include:

- utils: Carpeta que contiene un archivo `funcniones.py` con funciones reutilizables por el webscraper y transformaciones finales utilizadas para realizar la predicción del precio del vehículo.

- model: Carpeta que contiene el modelo final utilizado para realizar la predicción del precio del vehículo.

- data: Datos del dataset de Kaggle utilizado como origen de datos (además de los scrapeados) y de pruebas y trasnformaciones llevadas a cabo en los notebooks.

- db_*.db: Estos archivos son la base de datos de tipo SQLite que utilizamos para guardar todos los registros y su Backup.

### `requirements.txt`
Lista de dependencias necesarias para ejecutar el proyecto.
