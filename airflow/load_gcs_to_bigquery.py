import os
import datetime
from dotenv import load_dotenv
from airflow import DAG
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator

# Charger les variables d'environnement
load_dotenv()

GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
BQ_DATASET = os.getenv("BQ_DATASET")
BQ_TABLE = os.getenv("BQ_TABLE")
GCS_BUCKET = os.getenv("GCS_BUCKET_COMPOSER")

default_args = {
    'start_date': datetime.datetime(2024, 3, 1),
    'retries': 1,
    'retry_delay': datetime.timedelta(minutes=5),
}

dag = DAG(
    'load_gcs_to_bigquery',
    default_args=default_args,
    description='Load CSV file from GCS to BigQuery',
    schedule_interval='@hourly',
    catchup=False,
)

gcs_to_bq = GCSToBigQueryOperator(
    task_id='gcs_to_bq',
    bucket=GCS_BUCKET,
    source_objects=['data/my_data.csv'],  # Fichier CSV dans GCS
    destination_project_dataset_table=f'{GCP_PROJECT_ID}.{BQ_DATASET}.{BQ_TABLE}',
    write_disposition='WRITE_TRUNCATE',  # Écrase la table existante
    skip_leading_rows=1,  # Ignore la première ligne (en-têtes)
    field_delimiter=',',
    source_format='CSV',
    dag=dag,
)

gcs_to_bq
