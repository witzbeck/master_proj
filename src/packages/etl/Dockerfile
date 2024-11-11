FROM python:3.12-alpine AS base

ARG uv_version=0.5.4

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

RUN apk update && \
    apk add libpq


FROM base AS builder

RUN apk update && \
    apk add musl-dev build-base gcc gfortran openblas-dev

WORKDIR /app

# Install Poetry
RUN pip install uv==$uv_version

# Install the app
COPY pyproject.toml uv.lock ./
RUN uv sync --locked

FROM base AS runtime

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY src ./src

WORKDIR /app/src

ENTRYPOINT ["poetry", "run", "pipe-etl"]