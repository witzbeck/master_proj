FROM postgres:16.2-alpine

# Copy config and source data to the container
#COPY ./database/postgres-$ENVIRONMENT.conf /etc/postgresql/postgresql.conf
COPY ./database/source_data /source_data

# Copy the database schema to the container
COPY ./init-scripts /docker-entrypoint-initdb.d/schema.sql
