select
    act.activity_type,
    act.id activity_type_id,
    svb.date activity_date,
    ast.assessment_type,
    ast.id assessment_type_id,
    a.assessment_date,
    a.assessment_date - svb.date activity_days_before_due,
    a.assessment_weight,
    si.final_result_id,
    fr.final_result,
    sab.date_submitted,
    sab.date_submitted - a.assessment_date days_submitted_early,
    svb.sum_click,
    si.id student_id,
    si.imd_band_id,
    si.highest_education_id,
    he.highest_education,
    si.region_id,
    si.is_female,
    si.has_disability,
    si.age_band_id,
    ab.age_band
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
    join main.assessment a
        on
            a.assessment_id = sab.assessment_id
            and a.course_id = scb.course_id
    join main.activity_type act on act.id = vcb.activity_type_id
    join main.assessment_type ast on ast.id = a.assessment_type_id
    join main.age_band ab on ab.id = si.age_band_id
    join main.final_result fr on fr.id = si.final_result_id
    join main.highest_education he on he.id = si.highest_education_id
where
    sab.date_submitted - a.assessment_date > 0
    and a.assessment_date - svb.date > 0;
