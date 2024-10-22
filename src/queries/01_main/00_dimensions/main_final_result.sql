SELECT
    row_number() OVER (
        ORDER BY final_result
    ) id,
    final_result
FROM landing.student_info
WHERE final_result IS NOT null
GROUP BY final_result
ORDER BY final_result;
