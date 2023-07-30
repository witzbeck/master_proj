with revisits as ( 
    select student_id
    ,site_id
    ,sum(is_revisits) n_revisits     
    from (
                    select
                     i.student_id
                    ,i.course_id
                    ,i.site_id
                    ,i.date
                    ,i.activity_type
                    ,row_number() over (partition by student_id, site_id order by date) order_visited
                    ,1 is_revisits
                    from first30.interactions i
                    group by i.student_id
                    ,i.course_id
                    ,i.site_id
                    ,i.date
                    ,i.activity_type
                    ) a
                    where order_visited > 1
                    and activity_type not in ('homepage')
                    group by student_id, site_id
                    )

select
 i.student_id
,i.course_id
,count(distinct i.date)     n_days_active
,max(i.sum_click)           max_clicks_any_activity
,sum(n_revisits)            n_revisits_total
,max(n_revisits)            max_revisits_total

into first30.activities_revisits
from first30.interactions i
join revisits r on r.student_id=i.student_id
group by  i.student_id
         ,i.course_id
