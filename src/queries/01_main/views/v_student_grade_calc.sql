select
    scb.student_id,
    scb.module_id,
    scb.presentation_id,
    sum(a.date * a.weight) / sum(a.date) assessment_weight_date_rate,
    sum(a.weight) sum_weight,
    sum(sab.score * a.weight) score_weight_product,
    sum(
        case
            when a.date is null then 0
            else a.date - sab.date_submitted
        end
    ) days_submitted_early,
    count(*) n_assessments,
    sum(a.weight * (a.date - sab.date_submitted)) days_early_weight_product,
    sum(a.weight * (a.date - sab.date_submitted)) / sum(a.weight) days_early_per_weight_rate,
    f.final_result,
    case
        when f.final_result = 'Withdrawn' then null
        else sum(sab.score * a.weight) / sum(a.weight)
    end final_grade,
    sum(
        case
            when a.date is null then 0
            else a.date - sab.date_submitted
        end
    ) / count(*) avg_days_submitted_early
from main.student_info si
    join main.student_vle_bridge scb on si.id = scb.student_id
    join main.student_assessment_bridge sab on sab.student_id = si.id
    join main.assessment_info a
        on
            a.assessment_id = sab.assessment_id
            and a.module_id = scb.module_id
            and a.presentation_id = scb.presentation_id
    join main.final_result f on f.id = si.final_result_id
    join main.assessment_types t on t.id = a.assessment_type_id
where a.weight > 0
group by
    scb.student_id,
    scb.module_id,
    scb.presentation_id,
    f.final_result
