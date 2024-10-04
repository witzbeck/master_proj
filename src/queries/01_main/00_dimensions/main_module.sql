SELECT
    row_number() OVER (
        ORDER BY code_module
    ) id,
    code_module module_code
FROM landing.courses
WHERE code_module IS NOT NULL
GROUP BY code_module
ORDER BY code_module;
