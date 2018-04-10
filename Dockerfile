FROM mariadb:latest

FROM python:3.4

RUN apt-get update && \
    apt-get install -y \
    --no-install-recommends mysql-client \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y mariadb-server \
    && rm -rf /var/lib/mysql && mkdir -p /var/lib/mysql /var/run/mysqld \
    && chown mysql:mysql -R /var/lib/mysql /var/run/mysqld \
    && chmod 777 /var/run/mysqld \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt ./


COPY . .