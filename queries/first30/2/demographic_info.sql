select *
into first30.demographic_info
from feat.demographic_info a 
join first30.student_ids i on i.id=a.student_id