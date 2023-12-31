# Commoncrawl Analysis

## Prerequisites
- A Google account (to create ressources in GCP)
- A Prefect account (with access to the Prefect Cloud)
- A Free Neo4J Aura instance (can be easily setup on [Neo4j site](https://console.neo4j.io/))
- VS Code with Devcontainer installed 
- Expects the following Git branches. See [Git Branching Strategy](https://github.com/m-p-esser/common_crawl/blob/master/docs/images/Data_Engineering_Git_Branching_Strategy.png):
  - master
  - develop
  - test 

## Folder structure

*hint: `tree -L 2 -d -A`* 

```
.
├── data             --> Data in different stages (raw, staged, final)
│   ├── 00_raw       --> Immutable, raw data
│   ├── 01_staged    --> Processed data
│   └── 02_final     --> Data which can be served (ML, Analytics)
├── deployments      --> Prefect deployment .yaml files
├── docs
│   └── images
├── images           --> Collection of Docker images
│   ├── prefect-agent
│   └── prefect-worker
├── infrastructure   --> Terraform infra configs and scripts
│   ├── compute
│   └── storage
├── make             --> Makefiles for setting up ressources and environment
│   └── prefect
├── notebooks        --> Jupyter or Observeable (JS) Notebooks
├── output           --> Deliverables in form of reports or models
│   ├── models
│   └── reports
├── src              --> Source code (Python, JS)
│   ├── commoncrawl
│   └── prefect
├── tests            --> Unit tests
└── workflows        --> Github actions (CI)
```

## Setup

### Environment Setup
*necessary everytime you start working on the project*
1. `make env-init` to setup environment
2. `make dev-init` to setup development environment
3. Start Docker Daemon
4. Rebuild and reopen in container

### GCP Setup
1. Define values in base.env (not part of this repository)
2. Run `make setup-gcp` to setup up the Google Cloud Project

If this doesn't work, run the commands from `01_00_setup_gcp.mk` command by command in the following order:
- `make create-gcp-project`
- `make set-default-gcp-project`
- `make link-project-to-billing-account`
- `make create-deployment-service-account`
- `make create-deployment-service-account-key-file`
- `make enable-gcp-services`
- `make bind-iam-policies-to-deployment-service-account`

### Prefect Setup
As mentioned above, this project requires a Prefect account and access to the Prefect ckoud

Create Repository in Google Artifact Registry where you can deploy Docker images
1. `make create-blocks`
2. `make create-prefect-artifact-repository`

### Setup Storage
1. Setup the storage infrastructure by running
`cd/.infrastructure/storage`
2. `terraform init` to init Terraform
3. `terraform plan` to see planned changes
4. `terraform apply` to setup infrastructure as defined in `main.tf` files

### Deploy Flow
1. Build and push the docker image -> `make deploy-prefect-worker-image`
2. The deploy as Google Cloud Run Job -> `make deploy-gcr-flow`

## About the Common Crawl Project

Important File Types
- WAT
- WART
- WET

### WAT Files
https://gist.github.com/Smerity/e750f0ef0ab9aa366558#file-bbc-pretty-wat