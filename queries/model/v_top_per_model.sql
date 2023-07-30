select 
 a.model_type
,count(n) n_models
,sum(a.mean_test_roc_auc) / count(n) avg_mean_test_roc_auc    
,sum(a.std_test_roc_auc)  / count(n) avg_std_test_roc_auc    
,sum(a.mean_fit_time)     / count(n) avg_mean_fit_time        
,sum(a.std_fit_time)      / count(n) avg_std_fit_time
,sum(a.mean_score_time)   / count(n) avg_mean_score_time    
,sum(a.std_score_time)    / count(n) avg_std_score_time

from (
select
 row_number() over (PARTITION BY case when ru.model_type = 'svm' then 'svc' else ru.model_type end 
                        ORDER BY r.mean_test_roc_auc DESC) n
,case when ru.model_type = 'svm' then 'svc' else ru.model_type end model_type
,r.mean_fit_time
,r.std_fit_time
,r.mean_score_time
,r.std_score_time
,r.mean_test_roc_auc
,r.std_test_roc_auc
,r.rank_test_roc_auc
from model.results r
join model.runs ru on ru.id=r.run_id
where mean_test_roc_auc is not null
) a
where n between 15 and 34
GROUP BY a.model_type
ORDER BY avg_mean_test_roc_auc desc
