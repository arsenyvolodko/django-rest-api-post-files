FROM python:3.11-buster

RUN pip install poetry==1.7.1

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev --no-root

COPY django_api_files ./django_api_files

ENTRYPOINT ["poetry", "run", "gunicorn", "django_api_files.wsgi:application", "--bind", "91.201.113.17:8000"]