SELECT
    row_number() OVER (
        ORDER BY module_code
    ) id,
    module_code
FROM landing.courses
WHERE module_code IS NOT NULL
GROUP BY module_code
ORDER BY module_code;
