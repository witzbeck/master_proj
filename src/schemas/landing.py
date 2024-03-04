from sqlalchemy import Column, Float, Integer, String, SmallInteger
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Vle(Base):
    __tablename__ = "vle"
    site_id = Column(Integer)
    code_module = Column(String(45))
    code_presentation = Column(String(45))
    activity_type = Column(String(45))
    week_from = Column(SmallInteger)
    week_to = Column(SmallInteger)


class StudentVle(Base):
    __tablename__ = "studentVle"
    site_id = Column(Integer)
    student_id = Column(Integer)
    code_module = Column(String(45))
    code_presentation = Column(String(45))
    date = Column(Integer)
    sum_click = Column(Integer)


class StudentRegistration(Base):
    __tablename__ = "studentRegistration"
    code_module = Column(String(45))
    code_presentation = Column(String(45))
    student_id = Column(Integer)
    date_registration = Column(Integer)
    date_unregistration = Column(Integer)


class StudentInfo(Base):
    __tablename__ = "studentInfo"
    student_id = Column(Integer)
    code_module = Column(String(45))
    code_presentation = Column(String(45))
    gender = Column(String(3))
    imd_band = Column(String(16))
    highest_education = Column(String(45))
    age_band = Column(String(45))
    num_of_prev_attempts = Column(Integer)
    studied_credits = Column(Integer)
    region = Column(String(45))
    disability = Column(String(3))
    final_result = Column(String(45))


class StudentAssessment(Base):
    __tablename__ = "studentAssessment"
    student_id = Column(Integer)
    assessment_id = Column(Integer)
    date_submitted = Column(Integer)
    is_banked = Column(SmallInteger)
    score = Column(Float)


class Courses(Base):
    __tablename__ = "courses"
    code_module = Column(String(45))
    code_presentation = Column(String(45))
    module_presentation_length = Column(Integer)

    @property
    def start_year(self) -> int:
        return int(self.code_presentation[:4])

    @property
    def start_month(self) -> str:
        return "02" if self.code_presentation[-1] == "B" else "10"

    @property
    def start_date(self) -> str:
        return f"{self.start_year}-{self.start_month}-01"

    @property
    def domain(self) -> str:
        return "Social Science" if self.code_module in ["AAA", "BBB", "GGG"] else "STEM"

    @property
    def level(self) -> int:
        if self.code_module == "AAA":
            ret = 3
        elif self.code_module == "GGG":
            ret = 0
        else:
            ret = 1
        return ret


class Assessments(Base):
    __tablename__ = "assessments"
    id_assessment = Column(Integer)
    code_module = Column(String(45))
    code_presentation = Column(String(45))
    assessment_type = Column(String(45))
    date = Column(Integer)
    weight = Column(Integer)
