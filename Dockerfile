FROM python:3.10-slim

ENV POETRY_VIRTUALENVS_CREATE=false

RUN apt-get update && apt-get install -y \
    curl \
    libpq-dev \
    gcc \
    && apt-get clean

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY ./notification_service .
COPY ./config.yaml ./config.yaml

CMD ["python", "main.py"]