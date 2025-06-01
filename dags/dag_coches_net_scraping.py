from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def run_scraper():
    """Importa y ejecuta el script de scraping directamente."""
    exec(open(f"./include/utils/coches_net_scraper.py").read(), globals())

with DAG(
    dag_id='scraping_vehiculos_coches_net',
    default_args=default_args,
    description='Web scraping diario de vehículos de coches.net',
    schedule_interval='0 6 1 * *',  # Se ejecuta el día 1 de cada mes a las 6:00 AM
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['scraping', 'coches', 'segunda_mano'],
) as dag:

    ejecutar_scraping = PythonOperator(
        task_id='ejecutar_scraper_coches_net',
        python_callable=run_scraper,
    )

    ejecutar_scraping
