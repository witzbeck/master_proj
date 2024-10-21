SELECT
    row_number() OVER (
        ORDER BY assessment_type
    ) id,
    assessment_type
FROM landing.assessments
WHERE assessment_type IS NOT NULL
GROUP BY assessment_type
ORDER BY assessment_type;
