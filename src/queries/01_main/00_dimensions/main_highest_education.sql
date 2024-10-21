SELECT
    row_number() OVER (
        ORDER BY highest_education
    ) id,
    highest_education
FROM landing.student_info
WHERE highest_education IS NOT NULL
GROUP BY highest_education
ORDER BY highest_education;
