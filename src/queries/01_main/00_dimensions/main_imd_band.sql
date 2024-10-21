SELECT
    row_number() OVER (
        ORDER BY imd_band
    ) id,
    imd_band
FROM landing.student_info
WHERE imd_band IS NOT null
GROUP BY imd_band
ORDER BY imd_band;
