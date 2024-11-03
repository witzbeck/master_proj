# Base image for common dependencies
FROM python:3.13-alpine AS base

ARG DEV=false

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    DBPATH=/data/learning.db

# Update package index and install dependencies
RUN apk update && \
    apk add --no-cache libpq libstdc++ cmake make g++ apache-arrow apache-arrow-dev && \
    apk add --virtual .build-deps build-base

# Builder stage for installing the app dependencies
FROM base AS builder

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN apk update && \
    apk add musl-dev build-base gcc gfortran openblas-dev

WORKDIR /app

# Install Poetry
RUN pip install poetry==1.8.3
RUN pip install pipx

# Install the app dependencies with Poetry
COPY pyproject.toml poetry.lock ./
RUN if [ "$DEV" = "true" ]; then \
        poetry install --with dev --no-root && rm -rf $POETRY_CACHE_DIR; \
    else \
        poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR; \
    fi

# Activate virtual environment to run initialization scripts
RUN poetry shell
RUN python -m app create-schema -a
RUN python -m app load-landing-data
RUN python -m app load-schema -s main -s agg -s first30 -s feat

# Clean up build dependencies to reduce image size
RUN apk del .build-deps

# Runtime stage to execute the application
FROM base AS runtime

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY --from=builder /data/${DBPATH} /data/${DBPATH}

COPY src ./src

WORKDIR /app/src

ENTRYPOINT ["pipx", "run", "duckdb-server"]
