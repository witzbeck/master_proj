create view eval2.v_mean_std_results as
select
 v.model_type
,v.run_id
,v.iter_id
,v.mean_fit_time
,v.std_fit_time
,v.mean_score_time
,v.std_score_time
,v.mean_test_roc_auc
,v.std_test_roc_auc
--,v.inc_aca
--,v.inc_dem
--,v.inc_eng
--,v.inc_all
--,v.name
from eval.v_all_runs_results v
;