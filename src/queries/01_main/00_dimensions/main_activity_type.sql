SELECT
    row_number() OVER (
        ORDER BY activity_type
    ) id,
    activity_type
FROM landing.activity_types
WHERE activity_type IS NOT NULL
GROUP BY activity_type
ORDER BY activity_type;
