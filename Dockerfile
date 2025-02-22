FROM python:3.13-slim

RUN pip install poetry==1.8.3

WORKDIR /src

COPY pyproject.toml poetry.lock* /src/

RUN poetry install --no-root --no-dev

COPY app /src
