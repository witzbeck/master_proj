select r.model_type,
    ra.run_id,
    ra.iter_id,
    ra.mean_fit_time,
    ra.std_fit_time,
    ra.mean_score_time,
    ra.std_score_time,
    ra.split0_test_roc_auc,
    ra.split1_test_roc_auc,
    ra.split2_test_roc_auc,
    ra.split3_test_roc_auc,
    ra.split4_test_roc_auc,
    ra.split5_test_roc_auc,
    ra.split6_test_roc_auc,
    ra.split7_test_roc_auc,
    ra.split8_test_roc_auc,
    ra.split9_test_roc_auc,
    ra.mean_test_roc_auc,
    ra.std_test_roc_auc,
    ra.rank_test_roc_auc,
    r.timestamp
from eval.results_all ra
    join eval.runs r on r.id = ra.run_id
    join eval.features f on f.run_id = ra.run_id
    join (
        select run_id,
            iter_id,
            mean_fit_time,
            std_fit_time,
            mean_score_time,
            std_score_time,
            mean_test_roc_auc,
            std_test_roc_auc,
            row_number() over (
                partition by mean_test_roc_auc
                order by mean_fit_time,
                    std_test_roc_auc,
                    std_fit_time
            ) n
        from eval.results_all
    ) a on a.run_id = ra.run_id
    and a.iter_id = ra.iter_id
    and n = 1
order by mean_test_roc_auc desc