select
 f.course_id
,f.student_id
,f.activity_type_id
,f.site_id
,f.activity_type
,f.n_clicks
,f.n_visits
,case when f.top_student_activity_by_visits = 1 then 1 else 0 end top1_student_activity_by_visits
,case when f.top_student_activity_by_visits = 2 then 1 else 0 end top2_student_activity_by_visits
,case when f.top_student_activity_by_visits = 3 then 1 else 0 end top3_student_activity_by_visits
,case when f.top_student_activity_by_clicks = 1 then 1 else 0 end top1_student_activity_by_clicks
,case when f.top_student_activity_by_clicks = 2 then 1 else 0 end top2_student_activity_by_clicks
,case when f.top_student_activity_by_clicks = 3 then 1 else 0 end top3_student_activity_by_clicks
,case when f.bot_student_activity_by_visits = 1 then 1 else 0 end bot1_student_activity_by_visits
,case when f.bot_student_activity_by_visits = 2 then 1 else 0 end bot2_student_activity_by_visits
,case when f.bot_student_activity_by_visits = 3 then 1 else 0 end bot3_student_activity_by_visits
,case when f.bot_student_activity_by_clicks = 1 then 1 else 0 end bot1_student_activity_by_clicks
,case when f.bot_student_activity_by_clicks = 2 then 1 else 0 end bot2_student_activity_by_clicks
,case when f.bot_student_activity_by_clicks = 3 then 1 else 0 end bot3_student_activity_by_clicks
from agg.most_popular_activities f
where (f.top_student_activity_by_visits between 1 and 3
    or f.top_student_activity_by_clicks between 1 and 3
    or f.bot_student_activity_by_visits between 1 and 3
    or f.bot_student_activity_by_clicks between 1 and 3)
limit 1000;