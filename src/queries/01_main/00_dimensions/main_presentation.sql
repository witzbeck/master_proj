SELECT
    row_number() OVER (
        ORDER BY presentation_code
    ) id,
    presentation_code
FROM landing.courses
WHERE presentation_code IS NOT NULL
GROUP BY presentation_code
ORDER BY presentation_code;
