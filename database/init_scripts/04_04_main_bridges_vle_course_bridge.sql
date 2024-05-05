-- This script creates the main.vle_course_bridge table and populates it with data from the staging.vle table.

BEGIN;
CREATE TABLE main.vle_course_bridge (
    vle_course_bridge_id SERIAL PRIMARY KEY,
    site_id INTEGER PRIMARY KEY,
    course_id INTEGER NOT NULL,
    module_id INTEGER NOT NULL REFERENCES main.course_info(module_id),
    presentation_id INTEGER NOT NULL REFERENCES main.course_info(presentation_id),
    activity_type_id INTEGER NOT NULL REFERENCES main.activity_types(id),
    week_from DATE,
    week_to DATE
);

COMMIT;

BEGIN;
INSERT INTO main.vle_course_bridge (
    site_id,
    course_id,
    module_id,
    presentation_id,
    activity_type_id,
    week_from,
    week_to
)
SELECT DISTINCT
    v.site_id,
    c.course_id,
    c.module_id,
    c.presentation_id,
    a.activity_type_id,
    v.week_from,
    v.week_to
FROM staging.vle v
JOIN main.course_info c ON c.module_code = v.module_code AND c.presentation_code = v.presentation_code
JOIN main.activity_types a ON a.activity_type = v.activity_type;

COMMIT;
