FROM python:3.4


RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y mariadb-server \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt ./

RUN ls /etc/init.d
RUN service mysql start

RUN pip install -r requirements.txt
RUN mysqladmin create mail2
COPY . .