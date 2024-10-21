SELECT
    row_number() OVER (
        ORDER BY age_band
    ) id,
    age_band
FROM landing.student_info
WHERE age_band IS NOT null
GROUP BY age_band
ORDER BY age_band;
