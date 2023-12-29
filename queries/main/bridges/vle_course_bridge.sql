/*
drop table if exists main.vle_course_bridge cascade;
*/
select 
     site_id
    ,c.id course_id
    ,c.module_id
    ,c.presentation_id
    ,a.id activity_type_id
    ,week_from
    ,week_to
into main.vle_course_bridge
from staging."vle" v
join main.course_info c on c.module_code = v.code_module
                    and c.presentation_code=v.code_presentation
join main.activity_types a on a.activity_type=v.activity_type
;