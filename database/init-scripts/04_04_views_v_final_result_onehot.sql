create view main.v_final_result_onehot as
select
    id
    , case when final_result = 'Distinction' then 1 else 0 end is_distinction
    , case when final_result = 'Fail' then 1 else 0 end is_fail
    , case when final_result = 'Pass' then 1 else 0 end is_pass
    , case when final_result = 'Withdrawn' then 1 else 0 end is_withdrawn
    , final_result
from main.final_result
