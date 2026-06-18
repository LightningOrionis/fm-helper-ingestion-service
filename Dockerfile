FROM python:3.12

ENV PYTHONUNBUFFERED=1
ENV POETRY_HOME="/opt/poetry"
ENV POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_VIRTUALENVS_IN_PROJECT=false
ENV POETRY_NO_INTERACTION=1
ENV POETRY_VERSION=1.8.0
ENV PATH="$PATH:$POETRY_HOME/bin"

RUN mkdir /app
WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -
COPY pyproject.toml poetry.lock /app/
RUN poetry install

COPY . /app

CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
EXPOSE 8000

