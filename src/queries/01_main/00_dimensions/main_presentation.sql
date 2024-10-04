SELECT
    row_number() OVER (
        ORDER BY code_presentation
    ) id,
    code_presentation presentation_code
FROM landing.courses
WHERE code_presentation IS NOT NULL
GROUP BY code_presentation
ORDER BY code_presentation;
