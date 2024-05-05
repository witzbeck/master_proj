-- This script creates the necessary databases and schemas for the project

    CREATE DATABASE mlflow;
    CREATE DATABASE learning;
    
-- Connect to the 'learning' database to create schemas; note this part must be run separately after connecting to the 'learning' database
    \c learning;


-- Start a transaction to group the schema creation commands
    BEGIN;

-- Create schemas in the 'learning' database
    CREATE SCHEMA landing;
    CREATE SCHEMA staging;
    CREATE SCHEMA main;
    CREATE SCHEMA main_audit;
    CREATE SCHEMA main_archive;
    CREATE SCHEMA main_temp;
    CREATE SCHEMA agg;
    CREATE SCHEMA first30days;
    CREATE SCHEMA model;

-- Commit the transaction to finalize the changes
    COMMIT;