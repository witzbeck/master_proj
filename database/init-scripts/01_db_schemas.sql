-- Description: Create databases and schemas for the project
CREATE DATABASE mlflow;
CREATE DATABASE learning;

-- Description: Create schemas for the database
USE learning;
CREATE SCHEMA landing;
CREATE SCHEMA staging;
CREATE SCHEMA main;
CREATE SCHEMA main_audit;
CREATE SCHEMA main_archive;
CREATE SCHEMA main_temp;
CREATE SCHEMA agg;
CREATE SCHEMA first30days;
CREATE SCHEMA model;
