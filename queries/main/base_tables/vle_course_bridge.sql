drop table if exists main.vle_course_bridge cascade;
select 
     site_id
    ,c.id course_id
    ,a.id activity_type_id
    ,week_from
    ,week_to
into main.vle_course_bridge
from staging."vle" v
join main.course_info c on c.module_code = v.code_module
                    and c.presentation_code=v.code_presentation
join main.activity_types a on a.activity_type=v.activity_type
;
alter table main.vle_course_bridge 
add constraint fk_activity_type_id
foreign key (activity_type_id)
references main.activity_types(id);
