with clicks as (
with
    date_mod0 as (select floor(date / 3) d,
                         student_id,
                         total_clicks
                         from first30.clicks_per_date 
                         where date % 3 = 0
                         and date <= 30),
    date_mod1 as (select floor(date / 3) d,
                         student_id,
                         total_clicks
                         from first30.clicks_per_date 
                         where date % 3 = 1
                         and date <= 30),
    date_mod2 as (select floor(date / 3) d,
                         student_id,
                         total_clicks
                         from first30.clicks_per_date 
                         where date % 3 = 2
                         and date <= 30)
select
 m0.student_id
,m0.d
,(m0.total_clicks * m1.total_clicks * m2.total_clicks) prod_3_click
from date_mod0 m0
join date_mod1 m1 on m1.d=m0.d and m1.student_id=m0.student_id
join date_mod2 m2 on m2.d=m0.d and m2.student_id=m0.student_id
)

select
 c.student_id
,sum(c.prod_3_click) / count(*) mean_prod_3_click
into first30.prod_3_dates_seq
from clicks c
group by student_id
