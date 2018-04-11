FROM python:3.4

RUN apt-get update && \
    apt-get install -y \
    --no-install-recommends mysql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt ./


COPY . .