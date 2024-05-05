-- Set the schema
SET search_path TO landing;

-- Import data from assessments.csv into assessments
COPY assessments
FROM '../source_data/assessments.csv'
DELIMITER ','
CSV HEADER;

-- Import data from courses.csv into courses
COPY courses
FROM '../source_data/courses.csv'
DELIMITER ','
CSV HEADER;

-- Import data from studentAssessment.csv into studentAssessment
COPY studentAssessment
FROM '../source_data/studentAssessment.csv'
DELIMITER ','
CSV HEADER;

-- Import data from studentInfo.csv into studentInfo
COPY studentInfo
FROM '../source_data/studentInfo.csv'
DELIMITER ','
CSV HEADER;

-- Import data from studentRegistration.csv into studentRegistration
COPY studentRegistration
FROM '../source_data/studentRegistration.csv'
DELIMITER ','
CSV HEADER;

-- Import data from studentVle.csv into studentVle
COPY studentVle
FROM '../source_data/studentVle.csv'
DELIMITER ','
CSV HEADER;

-- Import data from vle.csv into vle
COPY vle
FROM '../source_data/vle.csv'
DELIMITER ','
CSV HEADER;

-- Reset the search_path
RESET search_path;
