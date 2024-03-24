select
    s.student_id
    , sum(s.weight) sum_weight
    , sum(s.score) sum_score
    , course_weight
    , case
        when course_weight > 0
        then sum(s.score * s.weight) / course_weight
        else 0
    end day30_grade

    , sum(case when is_weighted = 1 then s.score else 0 end) / n.dist avg_score_weighted
    , sum(case when is_weighted = 0 then s.score else 0 end) / n.dist avg_score_unweighted
    , sum(s.score) / n.dist avg_score_combined
    , sum(case when is_weighted = 1 then 1 else 0 end) / cast(n.dist as float) submitted_ratio_combined_weighted
    , sum(case when is_weighted = 0 then 1 else 0 end) / cast(n.dist as float) submitted_ratio_combined_unweighted
    , count(*) / cast(n.dist as float) submitted_ratio_combined
    , n.dist n_expected
    , sum(s.is_weighted) n_weighted
    , count(*) - sum(s.is_weighted) n_unweighted
    , min(s.days_before_due_submitted) min_days_before_due_submitted
    , max(s.days_before_due_submitted) max_days_before_due_submitted
from agg.assessment_staging s
    join (
        select
            count(distinct assessment_id) dist
            , sum(weight) course_weight
            , course_id
        from main.assessment_info
        where date <= 30
        group by course_id
    ) n on n.course_id = s.course_id
where s.date_due <= 30
group by student_id, n.dist, course_weight
