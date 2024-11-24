# Use Python 3.12 on Alpine Linux as the base image
FROM python:3.12-alpine AS base

# Update package index and install libpq (PostgreSQL client library)
RUN apk update && apk add --no-cache libpq

# Builder stage to build dependencies
FROM base AS builder

# Install build tools and development libraries
RUN apk add --no-cache musl-dev build-base gcc gfortran openblas-dev curl git

# Install 'uv' package manager
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Set virtual environment path and update PATH
ENV VIRTUAL_ENV=/.venv
# Add /root/.local/bin to PATH
ENV PATH="/root/.local/bin:$VIRTUAL_ENV/bin:$PATH"

# Copy dependency files to the container
COPY pyproject.toml uv.lock ./

# Copy source code needed for building packages
COPY src/packages ./src/packages
COPY src/queries ./src/queries

# Install dependencies using 'uv' with the locked versions
# -n == --no-cache
RUN uv sync -n --frozen --no-dev --no-editable --no-progress

# Runtime stage
FROM base AS runtime

# Set virtual environment path and update PATH
ENV VIRTUAL_ENV=/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy the virtual environment from the builder stage
COPY --from=builder /.venv /.venv

# Copy the application source code
COPY --from=builder /src ./src

RUN uv run get-data
