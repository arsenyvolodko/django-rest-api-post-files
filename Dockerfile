FROM python:3.11-buster

RUN pip install poetry==1.7.1

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root && rm -rf $POETRY_CACHE_DIR

COPY django_api_files ./django_api_files
COPY manage.py ./

CMD ["poetry", "run", "gunicorn", "django_api_files.wsgi:application", "--bind", "91.201.113.17:8000"]

#FROM python:3.11-buster
#
#RUN pip install poetry==1.7.1
#
#WORKDIR /app
#
#COPY pyproject.toml poetry.lock ./
#
#RUN poetry config virtualenvs.create false
#RUN poetry install --no-dev --no-root
#
#COPY django_api_files ./django_api_files
#
#ENTRYPOINT ["poetry", "run", "gunicorn", "django_api_files.wsgi:application", "--bind", "0.0.0.0:8000"]