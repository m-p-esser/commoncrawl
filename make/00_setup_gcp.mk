##@ [Google Cloud Platform: Setup]

.PHONY: create-gcp-project
create-gcp-project: ## Create new GCP Project
	@echo "Create new project"
	gcloud projects create $(GCP_PROJECT_ID)
	@echo "Check if project is created"
	gcloud projects describe $(GCP_PROJECT_ID)

.PHONY: set-default-gcp-project
set-default-gcp-project: ## Set new GCP Project as default
	@echo "Set the project for the current session"
	gcloud config set project $(GCP_PROJECT_ID)

.PHONY: link-project-to-billing-account 
link-project-to-billing-account: ## Link GCP Project to Billing account
	@echo "Get list of billing accounts"
	gcloud beta billing accounts list
	@echo "Link billing account to project"
	gcloud beta billing projects link $(GCP_PROJECT_ID) --billing-account=$(GCP_BILLING_ACCOUNT)
	@echo "Confirm billing account has been linked"
	gcloud beta billing accounts --project=$(GCP_PROJECT_ID) list

.PHONY: create-deployment-service-account
create-deployment-service-account: ## Create Deployment Service Account
	@echo "Create new Deployment Service account"
	gcloud iam service-accounts create $(GCP_DEPLOYMENT_SERVICE_ACCOUNT)

.PHONY: create-deployment-service-account-key-file
create-deployment-service-account-key-file: ## Create GCP Keyfile for Deployment SA
	@echo "Creating Keyfile for Deployment Service account"
	mkdir -p .secrets
	gcloud iam service-accounts keys create .secrets/deployment_sa_account.json \
		--iam-account=$(GCP_DEPLOYMENT_SERVICE_ACCOUNT)@$(GCP_PROJECT_ID).iam.gserviceaccount.com

.PHONY: set-deployment-service-account-as-default
set-deployment-service-account-as-default: ## Set Deployment SA as default
	gcloud auth activate-service-account $(GCP_DEPLOYMENT_SERVICE_ACCOUNT)@$(GCP_PROJECT_ID).iam.gserviceaccount.com --key-file .secrets/deployment_sa_account.json
	gcloud config set account $(GCP_DEPLOYMENT_SERVICE_ACCOUNT)@$(GCP_PROJECT_ID).iam.gserviceaccount.com

.PHONY: enable-gcp-services
enable-gcp-services: ## Enable GCP services
	@echo "Enabling GCP services..."
	gcloud services enable artifactregistry.googleapis.com \
		run.googleapis.com \
		appenginereporting.googleapis.com \
		compute.googleapis.com \
		cloudresourcemanager.googleapis.com \
		dataproc.googleapis.com \
		storage-component.googleapis.com

.PHONY: bind-iam-policies-to-deployment-service-account
bind-iam-policies-to-deployment-service-account: ## Bind IAM Policies to Service Account
	@echo "Bind IAM Policies to Service account $(GCP_DEPLOYMENT_SERVICE_ACCOUNT)"
	gcloud projects add-iam-policy-binding $(GCP_PROJECT_ID) --member=serviceAccount:$(GCP_DEPLOYMENT_SERVICE_ACCOUNT)@$(GCP_PROJECT_ID).iam.gserviceaccount.com --role="roles/artifactregistry.admin"
	gcloud projects add-iam-policy-binding $(GCP_PROJECT_ID) --member=serviceAccount:$(GCP_DEPLOYMENT_SERVICE_ACCOUNT)@$(GCP_PROJECT_ID).iam.gserviceaccount.com --role="roles/iam.serviceAccountUser" 
	gcloud projects add-iam-policy-binding $(GCP_PROJECT_ID) --member=serviceAccount:$(GCP_DEPLOYMENT_SERVICE_ACCOUNT)@$(GCP_PROJECT_ID).iam.gserviceaccount.com --role="roles/storage.objectAdmin"
	gcloud projects add-iam-policy-binding $(GCP_PROJECT_ID) --member=serviceAccount:$(GCP_DEPLOYMENT_SERVICE_ACCOUNT)@$(GCP_PROJECT_ID).iam.gserviceaccount.com --role="roles/storage.admin"  
	gcloud projects add-iam-policy-binding $(GCP_PROJECT_ID) --member=serviceAccount:$(GCP_DEPLOYMENT_SERVICE_ACCOUNT)@$(GCP_PROJECT_ID).iam.gserviceaccount.com --role="roles/bigquery.admin" 
	gcloud projects add-iam-policy-binding $(GCP_PROJECT_ID) --member=serviceAccount:$(GCP_DEPLOYMENT_SERVICE_ACCOUNT)@$(GCP_PROJECT_ID).iam.gserviceaccount.com --role="roles/appengine.appAdmin"
	gcloud projects add-iam-policy-binding $(GCP_PROJECT_ID) --member=serviceAccount:$(GCP_DEPLOYMENT_SERVICE_ACCOUNT)@$(GCP_PROJECT_ID).iam.gserviceaccount.com --role="roles/run.admin"
	gcloud projects add-iam-policy-binding $(GCP_PROJECT_ID) --member=serviceAccount:$(GCP_DEPLOYMENT_SERVICE_ACCOUNT)@$(GCP_PROJECT_ID).iam.gserviceaccount.com --role="roles/compute.admin"
	gcloud projects add-iam-policy-binding $(GCP_PROJECT_ID) --member=serviceAccount:$(GCP_DEPLOYMENT_SERVICE_ACCOUNT)@$(GCP_PROJECT_ID).iam.gserviceaccount.com --role="roles/dataproc.worker"
# Grant your Google Account a role that lets you use the service account's roles and attach the service account to other resources:
	gcloud iam service-accounts add-iam-policy-binding $(GCP_DEPLOYMENT_SERVICE_ACCOUNT)@$(GCP_PROJECT_ID).iam.gserviceaccount.com --member="user:emarcphilipp@gmail.com" --role=roles/iam.serviceAccountUser

.PHONY: setup-gcp
setup-gcp: ## Setup GCP Project so it can be used for development, CI or production
	@echo "Setting up GCP Project"
	"$(MAKE)" create-gcp-project
	"$(MAKE)" set-default-gcp-project
	"$(MAKE)" link-project-to-billing-account
	"$(MAKE)" create-deployment-service-account
	"$(MAKE)" create-deployment-service-account-key-file
	"$(MAKE)" enable-gcp-services
	"$(MAKE)" bind-iam-policies-to-deployment-service-account
	"$(MAKE)" set-deployment-service-account-as-default
	@echo "Finished setting up GCP Project"