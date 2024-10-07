select *
from (
        select row_number() over (
                partition by v.model_type,
                a.course_id --,a.run_id
                --,a.iter_id   
                order by v.model_type,
                    a.course_id --,a.run_id
                    --,a.iter_id   
            ) n,
            a.course_id,
            a.run_id,
            a.iter_id,
            a.index,
            a.is_stem is_stem_abroca,
            a.is_female is_female_abroca,
            a.has_disability has_disability_abroca,
            v.model_type,
            v.mean_fit_time,
            v.std_fit_time,
            v.mean_score_time,
            v.std_score_time,
            v.mean_test_roc_auc,
            v.std_test_roc_auc,
            v.rank_test_roc_auc,
            v.timestamp,
            v.inc_aca,
            v.inc_dem,
            v.inc_eng,
            v.inc_all,
            v.name,
            r.n_students,
            r.n_females,
            r.n_disabled,
            r.is_stem course_is_stem,
            r.female_ratio,
            r.disabled_ratio,
            w.warnings
        from eval.abroca a
            join eval.all_runs_results v on v.run_id = a.run_id
            and v.iter_id = a.iter_id
            join first30.all_classes_ratios r on r.course_id = a.course_id
            left join eval.warnings w on w.run_id = a.run_id
    ) a
where mean_test_roc_auc > 0
    and is_female_abroca > 0
    and n = 1