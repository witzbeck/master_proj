CREATE TABLE main.activity_types (
    id SERIAL PRIMARY KEY,
    activity_type VARCHAR(14) NOT NULL
);
INSERT INTO main.activity_types (activity_type)
SELECT DISTINCT activity_type
FROM staging."vle"
ORDER BY activity_type;
