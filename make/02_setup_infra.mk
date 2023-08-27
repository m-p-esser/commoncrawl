##@ [Infrastructure: Setup]

.PHONY: create-environment-yaml
create-environment-yaml: ### Create environment.yaml using pyproject.toml as base
	poetry export -o requirements.txt --without-hashes --without-urls --without=dev,test
	python3 src/scripts/requirements_to_conda_env.py
	gsutil rm -r gs://${SPARK_STAGING_BUCKET_NAME}
	gsutil mb -c standard -l ${GCP_DEFAULT_REGION} gs://${SPARK_STAGING_BUCKET_NAME}
	gsutil cp environment.yaml gs://${SPARK_STAGING_BUCKET_NAME}/environment.yaml

.PHONY: create-spark-cluster 
create-spark-cluster: ## Create GCP Dataproc (Spark) Cluster
	gcloud dataproc clusters create ${SPARK_CLUSTER_NAME} \
	--region=northamerica-northeast2 \
	--service-account=$(GCP_DEPLOYMENT_SERVICE_ACCOUNT)@$(GCP_PROJECT_ID).iam.gserviceaccount.com \
	--image-version=2.0 \
	--bucket=${SPARK_STAGING_BUCKET_NAME}

# --properties='dataproc:conda.env.config.uri=gs://${SPARK_CLUSTER_NAME}/environment.yaml'
