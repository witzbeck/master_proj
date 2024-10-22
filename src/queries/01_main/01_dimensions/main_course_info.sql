select row_number() over () id,
    m.id module_id,
    p.id presentation_id,
    m.module_code,
    p.presentation_code,
    left(p.presentation_code, 4) presentation_year,
    case
        when right(p.presentation_code, 1) = 'B' then 'February'
        else 'October'
    end start_month,
    case
        when (
            right(p.presentation_code, 1) = 'B'
            and left(p.presentation_code, 4) = '2013'
        ) then '2013-02'
        when (
            right(p.presentation_code, 1) = 'J'
            and left(p.presentation_code, 4) = '2013'
        ) then '2013-10'
        when (
            right(p.presentation_code, 1) = 'B'
            and left(p.presentation_code, 4) = '2014'
        ) then '2014-02'
        when (
            right(p.presentation_code, 1) = 'J'
            and left(p.presentation_code, 4) = '2014'
        ) then '2014-10'
        else null
    end start_date,
    module_presentation_length,
    case
        when m.module_code in ('AAA', 'BBB', 'GGG') then 'Social Sciences'
        else 'STEM'
    end AS domain,
    case
        when m.module_code = 'AAA' then 3
        when m.module_code = 'GGG' then 0
        else 1
    end AS level
from landing.courses c
    join main.module m on m.module_code = c.module_code
    join main.presentation p on p.presentation_code = c.presentation_code
order by start_date;