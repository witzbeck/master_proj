FROM python:3.12-alpine as base

ARG DEV=false
ARG poetry_version=1.8.3

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

RUN apk update && \
    apk add libpq


FROM base as builder

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN apk update && \
    apk add musl-dev build-base gcc gfortran openblas-dev

WORKDIR /app

# Install Poetry
RUN pip install poetry==$poetry_version

# Install the app
COPY pyproject.toml poetry.lock ./
RUN if [ "$DEV" = "true" ]; then \
      poetry install --with dev --no-root && rm -rf $POETRY_CACHE_DIR; \
    else \
      poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR; \
    fi


FROM base as runtime

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY src ./src

WORKDIR /app/src

ENTRYPOINT ["poetry", "run", "pipe-etl"]