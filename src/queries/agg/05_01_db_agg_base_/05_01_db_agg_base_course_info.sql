CREATE TABLE agg.avg_course_lengths (
    course_id INTEGER PRIMARY KEY REFERENCES main.course_info(course_id),
    avg_module_length DECIMAL,
    avg_presentation_length DECIMAL
);

INSERT INTO agg.avg_course_lengths
select
    vc.course_id
    , m.avg_module_length
    , p.avg_presentation_length
from main.course_info vc
    join (
        select
            vc.module_id
            , sum(vc.module_presentation_length) / count(*) avg_module_length
        from main.course_info vc
        group by vc.module_id
    ) m on m.module_id = vc.module_id
    join (
        select
            vc.presentation_id
            , sum(vc.module_presentation_length) / count(*) avg_presentation_length
        from main.course_info vc
        group by vc.presentation_id
    ) p on p.presentation_id = vc.presentation_id
;
