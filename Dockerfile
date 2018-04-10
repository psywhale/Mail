FROM mariadb:latest

ENV MYSQL_ROOT_PASSWORD testjenkins
ENV MYSQL_DATABASE mail2
EXPOSE 3306



FROM python:3.4


RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    --no-install-recommends mysql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt ./


RUN pip install -r requirements.txt

COPY . .