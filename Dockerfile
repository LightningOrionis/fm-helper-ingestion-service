FROM python:3.12

ARG ENVIRONMENT=production

ENV PYTHONUNBUFFERED=1
ENV POETRY_HOME="/opt/poetry"
ENV POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_VIRTUALENVS_IN_PROJECT=false
ENV POETRY_NO_INTERACTION=1
ENV POETRY_VERSION=2.4.1
ENV PATH="$PATH:$POETRY_HOME/bin"

RUN mkdir /app
WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -
COPY pyproject.toml poetry.lock /app/
RUN if [ "$ENVIRONMENT" = "local" ]; then \
        poetry install --no-root --with dev; \
    else \
        poetry install --no-root; \
    fi

COPY . /app

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
EXPOSE 8000
