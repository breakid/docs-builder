# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/engine/reference/builder/

FROM alpine

ENV \
    # Exposed port where documentation will be served
    LISTEN_PORT=8000 \
    # Suppress the warning about installing Python packages as root
    PIP_ROOT_USER_ACTION=ignore \
    # Prevents Python from writing pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    # Keeps Python from buffering stdout and stderr to avoid situations where
    # the application crashes without emitting any logs due to buffering
    PYTHONUNBUFFERED=1 \
    # Set the working directory
    WORKING_DIR=/build

ENV \
    # The path in the container where the generated documentation will be written
    OUTPUT_DIR=${WORKING_DIR}/site

EXPOSE ${LISTEN_PORT}

USER root

VOLUME ${WORKING_DIR}

WORKDIR ${WORKING_DIR}

# Install Python3 and Python dependencies
# Use a cache mount (i.e., `/root/.cache/pip`) to speed up subsequent builds
# Bind mount `requirements.txt` into the container to eliminate an unnecessary COPY command
RUN --mount=type=bind,source=requirements.txt,target=requirements.txt \
    --mount=type=cache,target=/root/.cache/pip \
    # Install Python dependencies
    apk add --no-cache --no-progress -q python3 py3-pip && \
    pip install -r requirements.txt --break-system-packages

# Install `terraform-docs` to `/opt/terraform-docs`
ARG TERRAFORM_DOC_VERSION=0.19.0
RUN mkdir -p /opt/terraform-docs && \
    wget https://github.com/terraform-docs/terraform-docs/releases/download/v${TERRAFORM_DOC_VERSION}/terraform-docs-v${TERRAFORM_DOC_VERSION}-linux-amd64.tar.gz -O - | tar -xzC /opt/terraform-docs && \
    ln -s /opt/terraform-docs/terraform-docs /usr/local/bin/terraform-docs

# Install `inframap` to `/opt/inframap`
ARG INFRAMAP_VERSION=0.7.0
RUN mkdir -p /opt/inframap && \
    # Install dependencies
    apk add --no-cache --no-progress -q graphviz ttf-dejavu && \
    wget https://github.com/cycloidio/inframap/releases/download/v${INFRAMAP_VERSION}/inframap-linux-amd64.tar.gz -O - | tar -xzC /opt/inframap && \
    ln -s /opt/inframap/inframap-linux-amd64 /usr/local/bin/inframap

COPY . .

# Ensure the entrypoint script is executable
RUN chmod +x ${WORKING_DIR}/entrypoint.sh

# When stopping a container, Docker will send SIGTERM to PID 1, wait 10 seconds (by default) for the container to
# shutdown gracefully, then send SIGKILL if it's still running
# Applications that won't respond to SIGTERM (e.g., ones that fork and no longer run as PID 1) will eventually be sent
# SIGKILL; explicitly setting the stop signal to SIGKILL eliminates the unnecessary 10 second wait
STOPSIGNAL SIGKILL

# Run the application
ENTRYPOINT [ "./entrypoint.sh" ]
