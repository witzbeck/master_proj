
select 

s.id student_id 
,g.sum_weight
,g.sum_score
,g.course_weight
,g.day30_grade
,g.avg_score_weighted
,g.avg_score_unweighted
,g.avg_score_combined
,g.submitted_ratio_combined_weighted
,g.submitted_ratio_combined_unweighted
,g.submitted_ratio_combined
,g.n_expected
,g.n_weighted
,g.n_unweighted
,g.min_days_before_due_submitted
,g.max_days_before_due_submitted
,p.n_total_clicks_by_top_5th_clicks
,p.n_total_clicks_by_top_5th_visits
,p.n_total_visits_by_top_5th_clicks
,p.n_total_visits_by_top_5th_visits
,p.n_distinct_top_5th_by_clicks
,p.n_distinct_top_5th_by_visits
,r.n_days_active
,r.max_clicks_any_activity
,r.n_revisits_total
,r.max_revisits_total
,d.mean_prod_3_click

into first30.all_engagement
from first30.student_ids s
left join first30.grades g on g.student_id=s.id
left join first30.activities_top_5th_perc p on p.student_id=s.id
left join first30.activities_revisits r on r.student_id=s.id
left join first30.prod_3_dates_seq d on d.student_id=s.id
