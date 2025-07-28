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
RUN microdnf install -y python3.12 python3.12-pip && \
    alternatives --install /usr/bin/python python /usr/bin/python3.12 1 && \
    python -m ensurepip && \
    python -m pip install --no-cache-dir pip setuptools && \
    microdnf clean all

# Crea un utente non privilegiato
RUN useradd -m -s /sbin/nologin appuser

# Imposta la directory di lavoro
WORKDIR /app

# Copia solo i file necessari nell'immagine
COPY app.py parser.py requirements.txt /app/
COPY templates /app/templates

# Installa le dipendenze e rimuovi pip/setuptools per ridurre superficie d'attacco
RUN python -m pip install --no-cache-dir -r requirements.txt && \
    rm -rf ~/.cache/pip && \
    microdnf remove -y python3.12-pip python3.12-setuptools && \
    microdnf clean all

# Esegui come utente non root
USER appuser

# Espone la porta 8080
EXPOSE 8080

# Avvia l'app Flask
ENTRYPOINT ["python", "app.py"]
