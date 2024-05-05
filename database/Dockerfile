FROM postgres:16.2

# # Declare build arguments
# ARG POSTGRES_USER
ARG POSTGRES_PASSWORD
# ENV POSTGRES_USER=$POSTGRES_USER
ENV POSTGRES_PASSWORD=$POSTGRES_PASSWORD
# ARG POSTGRES_DB
ARG ENVIRONMENT
RUN echo "ENVIRONMENT: $ENVIRONMENT"

# Set environment variables based on build arguments
# ENV POSTGRES_USER=$POSTGRES_USER
# ENV POSTGRES_PASSWORD=$POSTGRES_PASSWORD
# ENV POSTGRES_DB=$POSTGRES_DB

# Copy config to the container
COPY ./postgres-$ENVIRONMENT.conf /etc/postgresql/postgresql.conf

# Copy ource data to the container
COPY ./source_data /source_data

# Copy the initialization scripts to the container
COPY ./init_scripts/*.sql /docker-entrypoint-initdb.d/
COPY ./init_scripts/*.sh /docker-entrypoint-initdb.d/

