# Commoncrawl Analysis

## About the Common Crawl Project

Important File Types
- WAT
- WART
- WET

### WAT Files
https://gist.github.com/Smerity/e750f0ef0ab9aa366558#file-bbc-pretty-wat

## Prerequisites
- A Google account (to create ressources in GCP)
- A Prefect account (with access to the Prefect Cloud)
- A Free Neo4J Aura instance (can be easily setup on [Neo4j site](https://console.neo4j.io/))
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
├── infrastructure   --> Docker images to run infrastructure
│   ├── compute
│   └── storage
├── deployments      --> Prefect deployment .yaml files
├── docs
│   └── images
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
└── workflows        --> Github actions (e.g. CI)
```

## Setup

### Activate Pre-commit 
pre-commit install

### Environment Setup
*necessary everytime you start working on the project*
1. `make dev-init` to setup development environment

### Environment Variables
1. Define values in base.env (not part of this repository)

### GCP Setup
1. Run `make setup-gcp` to setup up the Google Cloud Project

If this doesn't work, run the commands from `00_00_setup_gcp.mk` command by command in the following order:
- `make create-gcp-project`
- `make set-default-gcp-project`
- `make link-project-to-billing-account`
- `make create-deployment-service-account`
- `make create-deployment-service-account-key-file`
- `make enable-gcp-services`
- `make bind-iam-policies-to-deployment-service-account`
- `make set-deployment-service-account-as-default`

### Prefect Setup
As mentioned above, this project requires a Prefect account and access to the Prefect ckoud

Create Repository in Google Artifact Registry where you can deploy Docker images
1. `make create-blocks`
2. `make create-prefect-artifact-repository`

### Setup Storage
1. Setup the storage infrastructure by running

### Deploy 
- Add description here

## Next Steps

### Pyspark and Prefect
Probably not compatible with Data Proc
https://medium.com/globalwork-data-driven-world/data-orchestration-using-prefect-and-pyspark-7321559864f7

### Infrastructure Setup (Data Proc)
- Export pyproject.toml as requirements.txt in 02_setup_infra.mk
- Create a Docker image with all dependencies and install requirements.txt (which will be used by Data Proc)
- Deploy Data Proc Cluster using Make target

Consider https://cloud.google.com/dataproc/docs/tutorials/python-configuration
Can poetry create an environment.yaml as well?

### Pipeline (Please stick to it)

Step 1
- Option 1: Store JSONL files in Object Storage (or directly as Parquet file)
- Option 2: Combine JSON files in a Parquet file and store in Object Storage

Step 2 (If Option 2 from Step 1 is choosen)
- Sync Parquet File to Bigquery (or maybe skip this step?)

Step 3
- Option 1: Load Parquet File and do Data Processing using Data Proc (https://cloud.google.com/dataproc/docs/tutorials/gcs-connector-spark-tutorial#python)
- Option 2: Load Bigquery Table and do Data Processing using Data Proc (https://cloud.google.com/dataproc/docs/tutorials/bigquery-connector-spark-example#pyspark)

In General
- Submit Job to Data Proc using [Python API](https://cloud.google.com/dataproc/docs/tutorials/python-library-example#submit_a_job) 

https://docs.docker.com/desktop/install/ubuntu/#install-docker-desktop
