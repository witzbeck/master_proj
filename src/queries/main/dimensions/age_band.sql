CREATE TABLE main.age_band (
    id SERIAL PRIMARY KEY,
    age_band VARCHAR(7) NOT NULL
);
INSERT INTO main.age_band (age_band)
SELECT DISTINCT age_band
FROM staging."studentInfo"
WHERE age_band IS NOT null
ORDER BY age_band;
