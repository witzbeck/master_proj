-- Connect to the 'learning' database to create schemas; note this part must be run separately after connecting to the 'learning' database
    \c learning;


-- Start a transaction to group the schema creation commands


-- Create schemas in the 'learning' database
    BEGIN;    CREATE SCHEMA landing;          COMMIT;
    BEGIN;    CREATE SCHEMA staging;          COMMIT;
    BEGIN;    CREATE SCHEMA main;             COMMIT;
    BEGIN;    CREATE SCHEMA main_audit;       COMMIT;
    BEGIN;    CREATE SCHEMA main_archive;     COMMIT;
    BEGIN;    CREATE SCHEMA main_temp;        COMMIT;
    BEGIN;    CREATE SCHEMA agg;              COMMIT;
    BEGIN;    CREATE SCHEMA model;            COMMIT;

-- Commit the transaction to finalize the changes