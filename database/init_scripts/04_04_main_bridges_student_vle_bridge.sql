-- This script creates the student_vle_bridge table and populates it with data from the studentVle table in the staging schema.
CREATE TABLE main.student_vle_bridge (
    student_vle_bridge_id SERIAL PRIMARY KEY,
    site_id INTEGER NOT NULL REFERENCES main.vle(site_id),
    student_id INTEGER NOT NULL REFERENCES main.student_info(student_id),
    course_id INTEGER NOT NULL REFERENCES main.course_info(course_id),
    module_id INTEGER NOT NULL REFERENCES main.module(module_id),
    presentation_id INTEGER NOT NULL REFERENCES main.presentation(presentation_id),
    date DATE,
    sum_click INTEGER
);

INSERT INTO main.student_vle_bridge (
    site_id,
    student_id,
    course_id,
    module_id,
    presentation_id,
    date,
    sum_click
)
SELECT DISTINCT
    s.site_id,
    si.student_id,
    si.course_id,
    m.module_id,
    p.presentation_id,
    s.date,
    s.sum_click
FROM staging.studentVle s
JOIN main.modules m ON m.module_code = s.code_module
JOIN main.presentations p ON p.presentation_code = s.presentation_code
JOIN main.student_info si ON si.orig_student_id = s.student_id
                             AND si.module_id = m.module_id
                             AND si.presentation_id = p.presentation_id;
