FROM django

WORKDIR /app

COPY requirements.txt requirements.txt
RUN python -m venv /tmp/venv && \
    . /tmp/venv/bin/activate && \
    pip install -r requirements.txt

EXPOSE 8000
CMD ["python","manage.py","makemigrations"]
CMD ["python","manage.py","migrate"]

