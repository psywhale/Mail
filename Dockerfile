FROM   django

RUN apt-get update \
    && apt-get upgrade \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .

EXPOSE 8000
CMD ["python","manage.py","makemigrations"]
CMD ["python","manage.py","migrate"]

