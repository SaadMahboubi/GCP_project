import os
import datetime
from dotenv import load_dotenv
from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator

# Charger les variables d'environnement
load_dotenv()

GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
BQ_DATASET = os.getenv("BQ_DATASET")

default_args = {
    'start_date': datetime.datetime(2024, 3, 1),
    'retries': 1,
    'retry_delay': datetime.timedelta(minutes=5),
}

dag = DAG(
    'bigquery_query_execution',
    default_args=default_args,
    description='Run a BigQuery query on a scheduled basis',
    schedule_interval='@daily',
    catchup=False,
)

bq_query = f"""
CREATE OR REPLACE TABLE `{GCP_PROJECT_ID}.{BQ_DATASET}.filtered_table` AS
SELECT name, age, ville
FROM `{GCP_PROJECT_ID}.{BQ_DATASET}.table_test`
WHERE age > 25
"""

run_query = BigQueryInsertJobOperator(
    task_id="run_bq_query",
    configuration={
        "query": {
            "query": bq_query,
            "useLegacySql": False,
        }
    },
    dag=dag,
)
