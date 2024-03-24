create view eval.v_features as
select
    v.column_name
    , v.ordinal_position
    , v.data_type
    , v.is_bool
    , v.is_id
    , v.is_obj
    , v.is_by_activity
    , v.is_student_info
    , v.is_moment
    , case
        when left(column_name, 7) in ('is_pass', 'is_with', 'is_fail', 'is_dist') then 1
        else 0
    end is_final_result
    , case
        when left(column_name, 15) = 'avg_interaction' then 1
        when right(column_name, 5) = 'types' then 1
        when right(column_name, 10) in ('activities', 'ons_clicks', 'ction_date') then 1
        when
            left(column_name, 7) in (
                'n_total', 'n_disti', 'n_days_', 'max_cli', 'n_revis', 'n_inter', 'mean_pr', 'max_rev'
            )
        then 1
        else 0
    end is_engagement
    , case
        when column_name in ('is_stem', 'course_level', 'studied_credits', 'num_of_prev_attempts', 'reg_date') then 1
        when
            left(column_name, 9) in (
                'submitted', 'avg_score', 'studied_c', 'sum_score', 'sum_weigh', 'course_we', 'n_assessm'
            )
        then 1
        when left(column_name, 5) in ('start', 'day30', 'modul') then 1
        when right(column_name, 9) = 'submitted' then 1
        else 0
    end is_academic
    , case
        when column_name in ('is_female', 'has_disability') then 1
        when left(column_name, 9) = 'is_region' then 1
        when
            left(column_name, 6) in (
                'n_expe'
                , 'n_weig'
                , 'n_unwe'
                , 'max_click'
                , 'is_0_1'
                , 'is_imd'
                , 'is_age'
                , 'is_hig'
                , 'n_asses'
                , 'n_inter'
                , ''
            )
        then 1
        else 0
    end is_demographics
from first30.v_all_feat_info_schema v
--where v.is_id = 0
--and v.is_by_activity = 0
--and v.is_obj = 0
where case
    when left(column_name, 5) in ('unreg', 'coeff', 'fp_co') then 1
    when right(column_name, 5) in ('fp_co', 'coeff', 'e_dif') then 1
    else 0
end = 0
