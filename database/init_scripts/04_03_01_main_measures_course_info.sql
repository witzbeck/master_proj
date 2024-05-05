BEGIN;
CREATE TABLE main.course_info (
    course_id SERIAL PRIMARY KEY,
    module_id INTEGER NOT NULL REFERENCES main.module(module_id),
    presentation_id INTEGER NOT NULL REFERENCES main.presentation(presentation_id),
    module_code VARCHAR(10) NOT NULL,
    presentation_code VARCHAR(10) NOT NULL,
    presentation_year INTEGER,
    start_month VARCHAR(20),
    start_date DATE,
    module_presentation_length INTEGER,
    domain VARCHAR(20),
    level INTEGER
);
COMMIT;
BEGIN;
INSERT INTO main.course_info (
    module_id,
    presentation_id,
    module_code,
    presentation_code,
    presentation_year,
    start_month,
    start_date,
    module_presentation_length,
    domain,
    level
)
SELECT DISTINCT
    m.module_id,
    p.presentation_id,
    c.module_code AS module_code,
    c.presentation_code AS presentation_code,
    LEFT(c.presentation_code, 4) AS presentation_year,
    CASE
        WHEN RIGHT(c.presentation_code, 1) = 'B' THEN 'February'
        ELSE 'October'
    END AS start_month,
    CASE
        WHEN (RIGHT(c.presentation_code, 1) = 'B' AND LEFT(c.presentation_code, 4) = '2013') THEN '2013-02-01'
        WHEN (RIGHT(c.presentation_code, 1) = 'J' AND LEFT(c.presentation_code, 4) = '2013') THEN '2013-10-01'
        WHEN (RIGHT(c.presentation_code, 1) = 'B' AND LEFT(c.presentation_code, 4) = '2014') THEN '2014-02-01'
        WHEN (RIGHT(c.presentation_code, 1) = 'J' AND LEFT(c.presentation_code, 4) = '2014') THEN '2014-10-01'
        ELSE NULL
    END AS start_date,
    c.module_presentation_length,
    CASE
        WHEN c.module_code IN ('AAA', 'BBB', 'GGG') THEN 'Social Sciences'
        ELSE 'STEM'
    END AS domain,
    CASE
        WHEN c.module_code = 'AAA' THEN 3
        WHEN c.module_code = 'GGG' THEN 0
        ELSE 1
    END AS level
FROM staging.courses c
JOIN main.module m ON m.module_code = c.module_code
JOIN main.presentation p ON p.presentation_code = c.presentation_code
ORDER BY start_date
;
COMMIT;
