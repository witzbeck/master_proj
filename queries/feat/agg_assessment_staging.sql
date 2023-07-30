drop table agg.assessment_staging cascade;
select distinct
 s.id student_id
,b.student_id orig_student_id
,a.course_id
,b.assessment_id
,a.assessment_type_id
,t.assessment_type
,b.score
,a.weight
,case when a.weight > 0 then 1 else 0 end is_weighted
,b.is_banked
,b.date_submitted
,a.date - b.date_submitted days_before_due_submitted
,a.date date_due
into agg.assessment_staging
from main.student_assessment_bridge b
join (select id, orig_student_id 
        from main.student_info
        group by id, orig_student_id
        ) s on s.orig_student_id=b.student_id
join main.assessment_info a on a.assessment_id=b.assessment_id
join main.assessment_types t on t.id=a.assessment_type_id

order by orig_student_id, assessment_id