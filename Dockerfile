FROM python:3.11-slim

WORKDIR /app

#RUN pip install celery
#RUN pip install gunicorn
#RUN pip install djangorestframework
#RUN pip install python-dotenv
#RUN pip install psycopg2-binary
#RUN pip install dj_database_url

RUN poetry shell
RUN poetry install --no-root

COPY . .

CMD ["gunicorn", "-b", "91.201.113.17:8000", "django_api_files.wsgi:application"]
