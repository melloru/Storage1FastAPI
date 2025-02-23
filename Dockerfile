FROM python:3.13-slim

RUN pip install poetry==1.8.3

WORKDIR /src

COPY pyproject.toml poetry.lock .

RUN poetry config virtualenvs.create false && poetry install --no-interaction

COPY app .
