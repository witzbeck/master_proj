with clicks as (
    with
    date_mod0 as (
        select
            floor(activity_date / 3) d,
            student_id,
            sum_click
        from main.v_student_interactions_by_assessments
        where
            activity_date % 3 = 0
            and activity_date <= 30
    ),

    date_mod1 as (
        select
            floor(activity_date / 3) d,
            student_id,
            sum_click
        from main.v_student_interactions_by_assessments
        where
            activity_date % 3 = 1
            and activity_date <= 30
    ),

    date_mod2 as (
        select
            floor(activity_date / 3) d,
            student_id,
            sum_click
        from main.v_student_interactions_by_assessments
        where
            activity_date % 3 = 2
            and activity_date <= 30
    )

    select
        m0.student_id
        , m0.d
        , (m0.sum_click * m1.sum_click * m2.sum_click) prod_3_click
    from date_mod0 m0
        join date_mod1 m1 on m1.d = m0.d and m1.student_id = m0.student_id
        join date_mod2 m2 on m2.d = m0.d and m2.student_id = m0.student_id
)

select
    c.student_id
    , sum(c.prod_3_click) / count(*) mean_prod_3_click
into agg.mean_prod_consec_days
from clicks c
group by student_id
;
