SELECT
    row_number() OVER (
        ORDER BY region
    ) id,
    region
FROM landing.region
WHERE region IS NOT null
GROUP BY region
ORDER BY region;
