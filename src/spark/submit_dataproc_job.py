""" Submit Prefect Flow to Dataproc Cluster"""

import json

from google.cloud import dataproc_v1
from google.cloud.dataproc_v1 import JobControllerClient
from google.oauth2.service_account import Credentials

from utils import load_env_variables


def build_credentials() -> Credentials:
    """Load Credentials from Service Account file"""
    with open(".secrets/deployment_sa_account.json") as fp:
        service_account_info = json.load(fp)
        credentials = Credentials.from_service_account_info(service_account_info)
        return credentials


def build_job_client(credentials: Credentials, region: str) -> JobControllerClient:
    """Build Data Proc Job Client"""
    job_client = dataproc_v1.JobControllerClient(
        credentials=credentials,
        client_options={"api_endpoint": f"{region}-dataproc.googleapis.com:443"},
    )
    return job_client


def submit_dataproc_job(
    job_client,
    cluster_name: str,
    bucket_name: str,
    pyspark_filename: str,
    region: str,
    project_id: str,
):
    """Submit Job to Dataproc Cluster"""
    job_config = {
        "placement": {"cluster_name": cluster_name},
        "pyspark_job": {
            "main_python_file_uri": f"gs://{bucket_name}/{pyspark_filename}"
        },
    }

    operation = job_client.submit_job_as_operation(
        request={"project_id": project_id, "region": region, "job": job_config}
    )

    response = operation.result()

    return response


if __name__ == "__main__":
    env_variables = load_env_variables()
    credentials = build_credentials()
    job_client = build_job_client(
        credentials=credentials, region="northamerica-northeast2"
    )
    submit_dataproc_job(
        job_client=job_client,
        cluster_name=env_variables["SPARK_CLUSTER_NAME"],
        bucket_name=env_variables["SPARK_STAGING_BUCKET_NAME"],
        pyspark_filename="hello_pyspark.py",
        region="northamerica-northeast2",
        project_id=env_variables["GCP_PROJECT_ID"],
    )
