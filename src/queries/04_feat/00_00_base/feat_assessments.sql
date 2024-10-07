select
    s.student_id
    , s.final_grade
    , s.n_assessments_per_expectation per_course_assignments_ratio
    , s.n_weighted
    , s.n_unweighted
    , m.n n_total
    , s.n_weighted / m.n weighted_ratio
    , s.n_unweighted / m.n unweighted_ratio
    , s.min_days_before_due_submitted min_days_early
    , s.max_days_before_due_submitted max_days_early
    , m.avg_days avg_days_early
    , m.var_days var_days_early
    , m.stddev_days stddev_days_early
    , m.skew_days skew_days_early
    , m.kurt_days kurt_days_early
    , m.fp_coeff fp_coeff_days_early
from agg.student_assessment_calcs s
    join agg.mom_1234_by_assessments m on m.student_id = s.student_id
