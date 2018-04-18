FROM python:3.5

RUN apt-get update && \
    apt-get install -y \
    --no-install-recommends mysql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt ./

RUN pip install -r requirements.txt
COPY . .