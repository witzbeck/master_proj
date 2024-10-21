select r.model_type_id,
    ra.run_id,
    ra.iter_id,
    ra.mean_fit_time,
    ra.std_fit_time,
    ra.mean_score_time,
    ra.std_score_time,
    ra.mean_test_roc_auc,
    ra.std_test_roc_auc,
    ra.rank_test_roc_auc,
    r.timestamp
from model.results ra
    join model.runs r on r.id = ra.run_id
    join model.features f on f.run_id = ra.run_id
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
        from model.results
    ) a on a.run_id = ra.run_id
    and a.iter_id = ra.iter_id
    and n = 1
order by ra.mean_test_roc_auc desc