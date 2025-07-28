# Base image with pinned SHA256 digest for reproducibility
# To update the digest, run:
#   docker pull oraclelinux:9-slim
#   docker inspect oraclelinux:9-slim --format='{{index .RepoDigests 0}}'
ARG BASE_IMAGE_NAME=oraclelinux
ARG BASE_IMAGE_TAG=9-slim
ARG BASE_IMAGE_DIGEST=sha256:5663c32905e22f7b8c88247bc55125d12fbe9b14c0bab5c766181e7266b46cf1
ARG BASE_IMAGE=${BASE_IMAGE_NAME}:${BASE_IMAGE_TAG}@${BASE_IMAGE_DIGEST}

FROM ${BASE_IMAGE} AS base

# Install Python 3.12 and pip

# Install Python 3.12 and pip
RUN microdnf install -y python3.12 python3.12-pip && \
    alternatives --install /usr/bin/python python /usr/bin/python3.12 1 && \
    python -m ensurepip && \
    python -m pip install --no-cache-dir pip setuptools && \
    microdnf clean all

# Create a minimal non-root service user with no home directory
RUN useradd --system --no-create-home --shell /sbin/nologinn appuser

# Set working directory
WORKDIR /app

# Copy application files and set permissions
RUN mkdir -p /app && chown appuser:appuser /app && chmod 700 /app
COPY --chown=appuser:appuser --chmod=0400 app.py parser.py requirements.txt /app/
COPY --chown=appuser:appuser --chmod=0700 templates /app/templates
RUN chmod 400 /app/templates/*.html

# Install application dependencies
# Use --no-cache-dir to avoid caching the packages and clean up pip cache to reduce image size
RUN python -m pip install --no-cache-dir -r requirements.txt && \
    rm -rf ~/.cache/pip && \
    microdnf remove -y python3.12-pip python3.12-setuptools && \
    microdnf clean all

# Note: We avoid 'dnf update' to keep builds reproducible. Instead, use updated base images with pinned digests.

# Set user to run the application
USER appuser

# exposed port
EXPOSE 8080

# Launch Flask app
ENTRYPOINT ["python", "app.py"]
