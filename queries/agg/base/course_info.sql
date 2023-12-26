drop table if exists agg.course_info cascade;
select
 vc.id course_id
,vc.module_id
,vc.presentation_id
,m.avg_module_length
,p.avg_presentation_length
,vc.module_code
,vc.presentation_code
,vc.presentation_year
,vc.start_month
,vc.start_date
,vc.module_presentation_length
,vc.domain
into agg.course_info
from main.course_info vc
join (
select
 vc.module_id
,sum(vc.module_presentation_length)/count(*) avg_module_length
from main.course_info vc
group by vc.module_id
) m on m.module_id=vc.module_id
join (
select
 vc.presentation_id
,sum(vc.module_presentation_length)/count(*) avg_presentation_length
from main.course_info vc
group by vc.presentation_id
) p on p.presentation_id=vc.presentation_id