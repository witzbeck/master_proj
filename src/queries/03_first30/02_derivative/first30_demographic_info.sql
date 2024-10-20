select
    si.id student_id
    , si.age_band_id
    , si.imd_band_id
    , si.highest_education_id
    , si.region_id
    , si.is_female
    , si.has_disability
from main.student_info si
    join first30.student_ids i on i.id = si.id
