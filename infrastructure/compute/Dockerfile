# Sourced from https://cloud.google.com/dataproc/docs/guides/dataproc-docker-yarn

FROM debian:10-slim

# Suppress interactive prompts.
ENV DEBIAN_FRONTEND=noninteractive

# Required: Install utilities required by Spark scripts.
RUN apt update && apt install -y procps tini

# Optional: Add extra jars.
ENV SPARK_EXTRA_JARS_DIR=/opt/spark/jars/
ENV SPARK_EXTRA_CLASSPATH='/opt/spark/jars/*'
RUN mkdir -p "${SPARK_EXTRA_JARS_DIR}"
COPY *.jar "${SPARK_EXTRA_JARS_DIR}"

# Optional: Install and configure Miniconda3.
ENV CONDA_HOME=/opt/miniconda3
ENV PYSPARK_PYTHON=${CONDA_HOME}/bin/python
ENV PYSPARK_DRIVER_PYTHON=${CONDA_HOME}/bin/python