create view main.v_student_grade_calc as
select
    scb.student_id
    , scb.module_id
    , scb.presentation_id
    , sum(a.date * a.weight) / sum(a.date) assessment_weight_date_rate
    , sum(a.weight) sum_weight
    , sum(sab.score * a.weight) score_weight_product
    , sum(case
        when a.date is null then 0
        else a.date - sab.date_submitted
    end) days_submitted_early
    , count(*) n_assessments
    , sum(a.weight * (a.date - sab.date_submitted)) days_early_weight_product
    , sum(a.weight * (a.date - sab.date_submitted)) / sum(a.weight) days_early_per_weight_rate
    , f.final_result
    , case
        when f.final_result = 'Withdrawn' then null
        else sum(sab.score * a.weight) / sum(a.weight)
    end final_grade
    , sum(case
        when a.date is null then 0
        else a.date - sab.date_submitted
    end) / count(*) avg_days_submitted_early

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
    scb.student_id
    , scb.module_id
    , scb.presentation_id
    , f.final_result


create view main.v_student_info as
select
    si.student_id
    , si.orig_student_id
    , si.course_id
    , a.age_band
    , i.imd_band
    , h.highest_education
    , r.region
    , f.final_result
    , si.is_female
    , si.has_disability
    , si.date_registration
    , si.date_unregistration
    , si.studied_credits
    , si.num_of_prev_attempts
    , c.module_code
    , c.presentation_code
    , c.presentation_year
    , c.start_month
    , c.module_presentation_length
    , c.domain
    , c.level
from main.student_info si
    join main.final_result f on f.id = si.final_result_id
    join main.region r on r.id = si.region_id
    join main.highest_education h on h.id = si.highest_education_id
    join main.imd_band i on i.id = si.imd_band_id
    join main.age_band a on a.id = si.age_band_id
    join main.course_info c on c.id = si.course_id

CREATE VIEW main.v_student_courses AS
SELECT

    si.student_id
    , si.module_id
    , si.presentation_id
    , f.final_result_id
    , a.age_band_id
    , ib.imd_band_id
    , he.highest_education_id
    , r.region_id
    , c.module_code
    , c.presentation_code
    , c.module_presentation_length
    , c.domain
    , c.start_month
    , c.presentation_year
    , f.final_result
    , a.age_band
    , si.num_of_prev_attempts
    , si.studied_credits
    , ib.imd_band
    , he.highest_education
    , r.region
    , si.is_female
    , si.has_disability

FROM main.student_info si
    JOIN main.course_info c
        ON
            c.module_id = si.module_id
            AND c.presentation_id = si.presentation_id
    JOIN main.final_result f ON f.final_result_id = si.final_result_id

    JOIN main.age_band a ON a.id = si.age_band_id
    JOIN main.imd_band ib ON ib.id = si.imd_band_id
    JOIN main.highest_education he ON he.id = si.highest_education_id
    JOIN main.region r ON r.id = si.region_id

create or replace view main.v_student_interactions_by_assessments as
select
    act.activity_type
    , act.activity_type_id
    , svb.date activity_date
    , ast.assessment_type
    , ast.assessment_type_id
    , a.date assessment_date
    , a.date - svb.date activity_days_before_due
    , a.weight assessment_weight
    , si.final_result_id
    , fr.final_result
    , sab.date_submitted
    , sab.date_submitted - a.date days_submitted_early
    , svb.sum_click
    , si.student_id
    , si.imd_band_id
    , si.highest_education_id
    , he.highest_education
    , si.region_id
    , si.is_female
    , si.has_disability
    , si.age_band_id
    , ab.age_band
from main.student_info si
    join main.student_vle_bridge svb on svb.student_id = si.id
    join main.vle_course_bridge vcb
        on
            vcb.site_id = svb.site_id
            and vcb.module_id = svb.module_id
            and vcb.presentation_id = svb.presentation_id
    join main.student_vle_bridge scb
        on
            scb.student_id = si.id
            and scb.module_id = svb.module_id
            and scb.presentation_id = svb.presentation_id
    join main.student_assessment_bridge sab on sab.student_id = si.id
    join main.assessment_info a
        on
            a.assessment_id = sab.assessment_id
            and a.course_id = scb.course_id
    join main.activity_types act on act.id = vcb.activity_type_id
    join main.assessment_types ast on ast.id = a.assessment_type_id
    join main.age_band ab on ab.id = si.age_band_id
    join main.final_result fr on fr.id = si.final_result_id
    join main.highest_education he on he.id = si.highest_education_id
where
    sab.date_submitted - a.date > 0
    and a.date - svb.date > 0
;
