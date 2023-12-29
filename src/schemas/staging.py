from sqlalchemy import Column, Integer, String, SmallInteger
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Vle(Base):
    __tablename__ = 'vle'
    site_id = Column(Integer, primary_key=True)
    code_module = Column(String(3))
    code_presentation = Column(String(5))
    activity_type = Column(String(14))
    week_from = Column(SmallInteger)
    week_to = Column(SmallInteger)


class StudentVle(Base):
    __tablename__ = 'studentVle'
    site_id = Column(Integer)
    student_id = Column(Integer)
    code_module = Column(String(3))
    code_presentation = Column(String(5))
    date = Column(Integer)
    sum_click = Column(Integer)


class StudentRegistration(Base):
    __tablename__ = 'studentRegistration'
    code_module = Column(String(3))
    code_presentation = Column(String(5))
    student_id = Column(Integer)
    date_registration = Column(Integer)
    date_unregistration = Column(Integer)


class StudentInfo(Base):
    __tablename__ = 'studentInfo'
    student_id = Column(Integer)
    code_module = Column(String(3))
    code_presentation = Column(String(5))
    is_female = Column(Integer)
    imd_band = Column(String(7))
    highest_education = Column(String(27))
    age_band = Column(String(5))
    num_of_prev_attempts = Column(Integer)
    studied_credits = Column(Integer)
    region = Column(String(20))
    has_disability = Column(Integer)
    final_result = Column(String(11))


class StudentAssessment(Base):
    __tablename__ = 'studentAssessment'
    student_id = Column(Integer)
    assessment_id = Column(Integer)
    date_submitted = Column(Integer)
    is_banked = Column(Integer)
    score = Column(SmallInteger)


class Courses(Base):
    __tablename__ = 'courses'
    code_module = Column(String(3))
    code_presentation = Column(String(5))
    module_presentation_length = Column(Integer)


class Assessments(Base):
    __tablename__ = 'assessments'
    assessment_id = Column(Integer)
    code_module = Column(String(3))
    code_presentation = Column(String(5))
    assessment_type = Column(String(4))
    date = Column(Integer)
    weight = Column(Integer)
