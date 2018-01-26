FROM django

WORKDIR /app


EXPOSE 8000
CMD ["python","manage.py","makemigrations"]
CMD ["python","manage.py","migrate"]

