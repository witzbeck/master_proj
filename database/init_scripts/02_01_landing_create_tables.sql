-- Create tables in the landing schema
BEGIN;

-- Create the schema
CREATE SCHEMA landing;

CREATE TABLE landing.vle (
    id_site INTEGER,
    code_module VARCHAR(45),
    code_presentation VARCHAR(45),
    activity_type VARCHAR(45),
    week_from TEXT,
    week_to TEXT
);

CREATE TABLE landing.studentVle (
    code_module VARCHAR(45),
    code_presentation VARCHAR(45),
    id_student INTEGER,
    id_site INTEGER,
    date INTEGER,
    sum_click INTEGER
);

CREATE TABLE landing.studentRegistration (
    code_module VARCHAR(45),
    code_presentation VARCHAR(45),
    id_student INTEGER,
    date_registration TEXT,
    date_unregistration TEXT
);

CREATE TABLE landing.studentInfo (
    code_module VARCHAR(45),
    code_presentation VARCHAR(45),
    id_student INTEGER,
    gender VARCHAR(3),
    region VARCHAR(45),
    highest_education VARCHAR(45),
    imd_band VARCHAR(16),
    age_band VARCHAR(45),
    num_of_prev_attempts INTEGER,
    studied_credits INTEGER,
    disability VARCHAR(3),
    final_result VARCHAR(45)
);

CREATE TABLE landing.studentAssessment (
    id_assessment INTEGER,
    id_student INTEGER,
    date_submitted INTEGER,
    is_banked SMALLINT,
    score TEXT
);

CREATE TABLE landing.courses (
    code_module VARCHAR(45),
    code_presentation VARCHAR(45),
    module_presentation_length INTEGER
);

CREATE TABLE landing.assessments (
    code_module VARCHAR(45),
    code_presentation VARCHAR(45),
    id_assessment INTEGER,
    assessment_type VARCHAR(45),
    date TEXT,
    weight TEXT
);

-- Commit the transaction to finalize imports
COMMIT;

