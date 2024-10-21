SELECT
    row_number() OVER (
        ORDER BY region
    ) id,
    region
FROM landing.student_info
WHERE region IS NOT null
GROUP BY region
ORDER BY region;
