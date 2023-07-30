alter table main.vle_course_bridge 
add constraint fk_activity_type_id
foreign key (activity_type_id)
references main.activity_types(id);
