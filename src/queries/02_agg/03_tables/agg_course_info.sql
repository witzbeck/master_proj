select
 vca.module_id
,vca.presentation_id
,vca.assessment_type_id
,sum(vca.assessment_date)                           sum_assessment_date
,count(*)                                           n_assessments
,sum(vca.assessment_weight)                         sum_assessment_weights
,sum(vca.assessment_date) / count(*)                avg_assessment_date 
,sum(vca.assessment_weight) / count(*)              avg_assessment_weight 
,sum(vca.assessment_weight * vca.assessment_date)   sum_weight_date_product
from main.course_assessments vca
join main.course_info c on c.module_id=vca.module_id
                    and c.presentation_id=vca.presentation_id          
group by
 vca.module_id
,vca.presentation_id
,vca.assessment_type_id