FROM python:3.12-slim-bookworm AS builder

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install tools + Java 21 (Temurin) + Node
RUN apt-get update && apt-get install -y --no-install-recommends \
        wget gnupg ca-certificates curl \
        gcc g++ make \
    && wget -O - https://packages.adoptium.net/artifactory/api/gpg/key/public | apt-key add - \
    && echo "deb https://packages.adoptium.net/artifactory/deb bookworm main" \
        > /etc/apt/sources.list.d/adoptium.list \
    && apt-get update && apt-get install -y --no-install-recommends \
        temurin-21-jdk \
        nodejs npm \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt /app/requirements.txt

RUN pip install --upgrade pip \
 && pip install --no-cache-dir --prefix=/usr/local -r /app/requirements.txt

COPY . /app

RUN chmod -R a+r /app || true


# ---------------- Production Image ----------------

FROM gcr.io/distroless/python3-debian12

WORKDIR /app

COPY --from=builder /usr/local /usr/local
COPY --from=builder /app /app

EXPOSE 8080

ENV APP_MODULE="app.main:app" \
    WORKERS="1" \
    GUNICORN_TIMEOUT="120" \
    BIND="0.0.0.0:8080" \
    GUNICORN_LOG_LEVEL="info"

ENTRYPOINT ["python3", "start.py"]
