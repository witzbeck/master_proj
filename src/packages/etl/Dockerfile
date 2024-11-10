# Use a lightweight Python base image
FROM python:3.11-slim

# Build-time arguments with default values
ARG EXPORT_WHOLE_DB=false
ARG EXPORT_TABLES=""
ARG DROP_TABLES=""
ARG LIMIT_PROCESSING=0
ARG INITIALIZE_SERVER=false

# Set environment variables based on ARGs
ENV EXPORT_WHOLE_DB=${EXPORT_WHOLE_DB}
ENV EXPORT_TABLES=${EXPORT_TABLES}
ENV DROP_TABLES=${DROP_TABLES}
ENV LIMIT_PROCESSING=${LIMIT_PROCESSING}
ENV INITIALIZE_SERVER=${INITIALIZE_SERVER}

# Install DuckDB and any other necessary Python packages
RUN pip install duckdb

# Create the app directory
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


FROM base AS runtime

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY src ./src

WORKDIR /app/src

ENTRYPOINT ["poetry", "run", "pipe-etl"]