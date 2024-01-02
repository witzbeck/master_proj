create view model.v_compare_perf as 
select
 b.id
,f.to_predict_col
,b.comb_order
,b.order_by_mean_fit_time
,b.order_by_mean_roc_auc
,b.model_type
,b.run_date
,b.mean_roc_auc
,b.mean_fit_time
,b.mean_accuracy

from (
select
sqrt(order_by_mean_fit_time) * sqrt(order_by_mean_roc_auc) comb_order
,*
from (
select
r.id
,row_number() over(order by s.mean_test_roc_auc desc) order_by_mean_roc_auc
,row_number() over(order by s.mean_fit_time) order_by_mean_fit_time
,r.model_type
,cast(r.timestamp as date) run_date
,cast(s.mean_test_roc_auc as numeric(8, 4)) mean_roc_auc
,cast(s.mean_fit_time as numeric(8,4)) mean_fit_time
,cast(s.mean_test_accuracy as numeric(8,4)) mean_accuracy
from model.runs r
join model.results s on s.run_id=r.id
where s.mean_test_roc_auc is not null
) a
) b
join model.feat f on f.run_id=b.id

order by comb_order