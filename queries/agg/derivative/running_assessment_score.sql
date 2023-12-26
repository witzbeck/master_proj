drop table if exists agg.running_assessment_score;
select *
,cum_score_weight_prod / cum_weight running_score

into agg.running_assessment_score
from (
    
select
 s.student_id
,s.course_id
,s.assessment_id
,s.assessment_type_id
,sum(s.score) over (partition by s.course_id, s.student_id
                     order by s.date_due) cum_score
,sum(s.weight) over (partition by s.course_id, s.student_id
                     order by s.date_due) cum_weight
,sum(s.score * s.weight) over (partition by s.course_id, s.student_id
                     order by s.date_due) cum_score_weight_prod
,s.weight
,s.is_banked
,s.date_due
from main.v_assessment_staging s

where s.is_weighted = 1
) s

order by 
 s.course_id
,s.student_id
,s.date_due