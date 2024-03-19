from pathlib import Path
from sqlalchemy import Column, Integer, String, SmallInteger
from sqlalchemy.orm import Session

from src.constants import DATA_PATH
from src.setup import Base

SCHEMA = Path(__file__).stem


class LandingTable(Base):
    __tablename__: str
    __table_args__ = {"schema": SCHEMA}

    def __str__(self) -> str:
        return f"{self.__table_args__['schema']}.{self.__tablename__}"

    @property
    def csv_path(self) -> Path:
        return DATA_PATH / f"{self.__tablename__}.csv"

    @property
    def copy_csv_str(self) -> str:
        return f"COPY {str(self)} FROM '{self.csv_path}' DELIMITER ',' CSV HEADER"

    @classmethod
    def seed_table(cls, session: Session) -> None:
        session.execute(cls.copy_csv_str)
        session.commit()


class Vle(Base, LandingTable):
    __tablename__ = "vle"
    site_id = Column(Integer)
    code_module = Column(String(3))
    code_presentation = Column(String(5))
    activity_type = Column(String(14))
    week_from = Column(SmallInteger)
    week_to = Column(SmallInteger)


class StudentVle(Base, LandingTable):
    __tablename__ = "studentVle"
    site_id = Column(Integer)
    student_id = Column(Integer)
    code_module = Column(String(3))
    code_presentation = Column(String(5))
    date = Column(Integer)
    sum_click = Column(Integer)


class StudentRegistration(Base, LandingTable):
    __tablename__ = "studentRegistration"
    code_module = Column(String(45))
    code_presentation = Column(String(45))
    student_id = Column(Integer)
    date_registration = Column(Integer)
    date_unregistration = Column(Integer)


class StudentInfo(Base, LandingTable):
    __tablename__ = "studentInfo"
    student_id = Column(Integer)
    code_module = Column(String(3))
    code_presentation = Column(String(5))
    gender = Column(String(1))
    imd_band = Column(String(7))
    highest_education = Column(String(27))
    age_band = Column(String(5))
    num_of_prev_attempts = Column(Integer)
    studied_credits = Column(Integer)
    region = Column(String(20))
    disability = Column(String(1))
    final_result = Column(String(11))


class StudentAssessment(Base):
    __tablename__ = "studentAssessment"
    student_id = Column(Integer)
    assessment_id = Column(Integer)
    date_submitted = Column(Integer)
    is_banked = Column(Integer)
    score = Column(SmallInteger)


class Courses(Base):
    __tablename__ = "courses"
    code_module = Column(String(3))
    code_presentation = Column(String(5))
    module_presentation_length = Column(Integer)


class Assessments(Base):
    __tablename__ = "assessments"
    id_assessment = Column(Integer)
    code_module = Column(String(3))
    code_presentation = Column(String(5))
    assessment_type = Column(String(4))
    date = Column(Integer)
    weight = Column(Integer)
