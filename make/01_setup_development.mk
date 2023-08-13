##@ [Development: Setup]

.PHONY: gcp-init
gcp-init: ## Set GCP Service account as standard service account
	gcloud auth login
	"$(MAKE)" set-default-gcp-project
	@echo "Configure Service Account to be active account. Required to work with GCP commands"
	"$(MAKE)" set-deployment-service-account-as-default
	gcloud config configurations list

.PHONY: env-init
env-init: ## Initialize environment, required everytime before the development process (whether you develop, test or hotfix)

	git init

	@echo "Setting environment"
	@$(eval current_branch=`git symbolic-ref --short HEAD`)
	@echo "Current branch: $(current_branch)"

	case $(current_branch) in \
		"develop") \
			echo "Development branch"; \
			echo "ENV=dev" > make/.env; \
			;; \
		"test") \
			echo "Test branch"; \
			echo "ENV=test" > make/.env; \
			;; \
		"master") \
			echo "Production branch"; \
			echo "ENV=prod" > make/.env; \
			;; \
		*) \
			echo "Unknown branch, using default values"; \
			echo "ENV=dev" > make/.env; \
			;; \
	esac;

.PHONY: dev-init
dev-init: ## Setup environment, so it can be used for dev, test or prod environment
	@echo "Activating Poetry Shell"
	poetry shell
	@echo "Set GCP Service account as standard service account"
	"$(MAKE)" gcp-init
	@echo "Logging into Prefect Cloud"
	prefect cloud login
	@echo "Set environment variable (dev, test or production)"
	"$(MAKE)" env-init