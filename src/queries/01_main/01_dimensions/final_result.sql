CREATE TABLE main.final_result (
    id SERIAL PRIMARY KEY,
    final_result VARCHAR(11) NOT NULL
);
INSERT INTO main.final_result (final_result)
SELECT DISTINCT final_result
FROM staging.studentinfo
WHERE final_result IS NOT null
ORDER BY final_result;
