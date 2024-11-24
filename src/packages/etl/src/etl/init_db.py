import os

import duckdb


def export_database(connection, output_path):
    # Export the entire database
    connection.execute(
        f"COPY (SELECT * FROM information_schema.tables) TO '{output_path}/database_export.csv' (FORMAT CSV, HEADER)"
    )
    print(f"Database exported to {output_path}/database_export.csv")


def export_tables(connection, tables, output_path):
    # Export specified tables
    for table in tables:
        connection.execute(
            f"COPY {table} TO '{output_path}/{table}.csv' (FORMAT CSV, HEADER)"
        )
        print(f"Table {table} exported to {output_path}/{table}.csv")


def drop_tables(connection, tables):
    # Drop specified tables
    for table in tables:
        connection.execute(f"DROP TABLE IF EXISTS {table}")
        print(f"Table {table} dropped")


def limit_processing(connection, limit):
    # Limit the number of schemas/stages executed
    # Placeholder for actual processing control logic
    print(f"Processing limited to {limit} schemas/stages")


def main():
    # Read environment variables
    export_whole_db = os.getenv("EXPORT_WHOLE_DB", "false").lower() == "true"
    export_tables_env = os.getenv("EXPORT_TABLES", "")
    export_tables = export_tables_env.split(",") if export_tables_env else []
    drop_tables_env = os.getenv("DROP_TABLES", "")
    drop_tables_list = drop_tables_env.split(",") if drop_tables_env else []
    limit_processing_env = os.getenv("LIMIT_PROCESSING", "0")
    limit_processing_value = (
        int(limit_processing_env) if limit_processing_env.isdigit() else 0
    )

    output_path = "/app/output"
    os.makedirs(output_path, exist_ok=True)

    # Connect to DuckDB (in-memory or specify a file)
    connection = duckdb.connect(database=":memory:")

    # Placeholder for database generation and population logic
    print("Generating and populating the DuckDB database...")

    # Handle environment variables to alter behavior
    if export_whole_db:
        export_database(connection, output_path)

    if export_tables:
        export_tables(connection, export_tables, output_path)

    if drop_tables_list:
        drop_tables(connection, drop_tables_list)

    if limit_processing_value > 0:
        limit_processing(connection, limit_processing_value)

    connection.close()


if __name__ == "__main__":
    main()
