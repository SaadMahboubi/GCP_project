import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator

# Charger les variables d'environnement
load_dotenv()

GKE_CLUSTER_NAME = os.getenv("GKE_CLUSTER_NAME")
GKE_NAMESPACE = os.getenv("GKE_NAMESPACE", "default")  # Namespace par défaut

default_args = {
    "start_date": datetime(2024, 3, 1),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "k8s_airflow_test",
    default_args=default_args,
    description="Run a simple test workload on Kubernetes via Airflow",
    schedule_interval="@daily",
    catchup=False,
)

run_k8s_task = KubernetesPodOperator(
    task_id="run_test_pod",
    name="test-pod",
    namespace=GKE_NAMESPACE,
    image="python:3.9",
    cmds=["python", "-c"],
    arguments=[
        "print('Hello from Kubernetes! Test réussi.')"
    ],
    dag=dag,
)

run_k8s_task
