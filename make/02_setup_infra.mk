##@ [Infrastructure: Setup]

.PHONY: export-requirements-txt 
export-requirements-txt: ### Create requirementxt.txt from pyproject.toml
	poetry export -o requirements.txt --without-hashes --without-urls --without=dev,test


.PHONY: create-spark-cluster 
create-spark-cluster: ## Create GCP Dataproc (Spark) Cluster
	gsutil rm -r gs://${SPARK_STAGING_BUCKET_NAME}
	gsutil mb -c standard -l northamerica-northeast2 gs://${SPARK_STAGING_BUCKET_NAME} 
	gcloud dataproc clusters create ${SPARK_CLUSTER_NAME} \
	--region=northamerica-northeast2 \
	--service-account=$(GCP_DEPLOYMENT_SERVICE_ACCOUNT)@$(GCP_PROJECT_ID).iam.gserviceaccount.com \
	--image-version=2.1-ubuntu20 \
	--master-machine-type=n1-standard-2 \
	--master-boot-disk-size 200 \
	--worker-machine-type=n1-standard-2 \
	--worker-boot-disk-size 200 \
	--bucket=${SPARK_STAGING_BUCKET_NAME} \
	--optional-components=JUPYTER \
	--enable-component-gateway \
	--metadata 'PIP_PACKAGES=google-cloud-storage'
	--initialization-actions gs://goog-dataproc-initialization-actions-northamerica-northeast2/python/pip-install.sh