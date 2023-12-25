drop table if exists main.course_info cascade;
select 
 row_number()over()         id
,m.id module_id
,p.id presentation_id
,code_module                module_code
,code_presentation          presentation_code
,left(code_presentation,4) presentation_year
,case
    when right(code_presentation,1) = 'B'
        then 'February'
    else 'October' end         start_month
,case 
    when (right(code_presentation,1) = 'B' and left(code_presentation,4) = '2013') then '2013-02'
    when (right(code_presentation,1) = 'J' and left(code_presentation,4) = '2013') then '2013-10'
    when (right(code_presentation,1) = 'B' and left(code_presentation,4) = '2014') then '2014-02'
    when (right(code_presentation,1) = 'J' and left(code_presentation,4) = '2014') then '2014-10'
    else null end           start_date
,module_presentation_length
,case
    when code_module in ('AAA', 'BBB', 'GGG')
        then 'Social Sciences'
    else 'STEM' end             domain
,case
    when code_module = 'AAA' then 3
    when code_module = 'GGG' then 0
    else 1 end            level
into main.course_info
from staging."courses" c
join main.modules m on m.module_code=c.code_module
join main.presentations p on p.presentation_code=c.code_presentation

order by start_date;