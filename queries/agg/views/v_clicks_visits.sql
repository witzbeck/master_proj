--drop table if exists agg.vle_interactions_staging;
SELECT

 b.student_id
,v.course_id
,sum(b.sum_click)           total_clicks
,count(*)                   total_visits
,count(distinct b.date)      distict_visits

--into agg.vle_interactions_staging
FROM main.student_vle_bridge b
JOIN main.vle_course_bridge v on b.site_id=v.site_id

group by  b.student_id
,v.course_id


