from sqlalchemy import (
    Column,
    Float,
    Integer,
    String,
    SmallInteger,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

from schemas.landing import Courses, StudentInfo, Vle

Base = declarative_base()


class Presentation(Base):
    __tablename__ = "presentation"
    id = Column(Integer, primary_key=True, autoincrement=True)
    presentation_code = Column(String(5), nullable=False)
    start_year = Column(Integer, nullable=False)
    start_month = Column(String(2), nullable=False)
    start_date = Column(String(10), nullable=False)
    __table_args__ = (
        UniqueConstraint(
            "presentation_code",
            "start_year",
            "start_month",
            "start_date",
            name="unique_presentation",
        ),
    )

    @classmethod
    def seed_table(cls, session: Session):
        all_presentations = session.query(Courses.code_presentation).distinct().all()
        session.add_all(
            [
                cls(presentation_code=presentation[0], start_month="February")
                for presentation in all_presentations
            ]
        )
        session.commit()


class Module(Base):
    __tablename__ = "module"
    id = Column(Integer, primary_key=True, autoincrement=True)
    module_code = Column(String(3), nullable=False)
    domain = Column(String(20), nullable=False)
    level = Column(SmallInteger, nullable=False)
    __table_args__ = (
        UniqueConstraint("module_code", "domain", "level", name="unique_module"),
    )

    @classmethod
    def seed_table(cls, session: Session):
        all_modules = session.query(Courses.code_module).distinct().all()
        session.add_all([cls(module_code=module[0]) for module in all_modules])
        session.commit()


class Course(Base):
    __tablename__ = "course"
    id = Column(Integer, primary_key=True, autoincrement=True)
    module_id = Column(Integer, ForeignKey("module.id"), nullable=False)
    presentation_id = Column(Integer, ForeignKey("presentation.id"), nullable=False)
    course_length = Column(Integer, nullable=False)


class ImdBand(Base):
    __tablename__ = "imd_band"
    id = Column(Integer, primary_key=True, autoincrement=True)
    imd_band = Column(String(7), nullable=False)

    @classmethod
    def seed_table(cls, session: Session):
        all_bands = session.query(StudentInfo.imd_band).distinct().all()
        session.add_all([cls(imd_band=band[0]) for band in all_bands])
        session.commit()

    @classmethod
    def get_id(cls, session: Session, band: str):
        return session.query(cls.id).filter(cls.imd_band == band).first()[0]


class AgeBand(Base):
    __tablename__ = "age_band"
    id = Column(Integer, primary_key=True, autoincrement=True)
    age_band = Column(String(7), nullable=False)

    @classmethod
    def seed_table(cls, session: Session):
        all_bands = session.query(StudentInfo.age_band).distinct().all()
        session.add_all([cls(age_band=band[0]) for band in all_bands])
        session.commit()

    @classmethod
    def get_id(cls, session: Session, band: str):
        return session.query(cls.id).filter(cls.age_band == band).first()[0]


class Region(Base):
    __tablename__ = "region"
    id = Column(Integer, primary_key=True, autoincrement=True)
    region = Column(String(20), nullable=False)

    @classmethod
    def seed_table(cls, session: Session):
        all_regions = session.query(StudentInfo.region).distinct().all()
        session.add_all([cls(region=region[0]) for region in all_regions])
        session.commit()

    @classmethod
    def get_id(cls, session: Session, region: str):
        return session.query(cls.id).filter(cls.region == region).first()[0]


class HighestEducation(Base):
    __tablename__ = "highest_education"
    id = Column(Integer, primary_key=True, autoincrement=True)
    highest_education = Column(String(27), nullable=False)

    @classmethod
    def seed_table(cls, session: Session):
        all_educations = session.query(StudentInfo.highest_education).distinct().all()
        session.add_all(
            [cls(highest_education=education[0]) for education in all_educations]
        )
        session.commit()

    @classmethod
    def get_id(cls, session: Session, education: str):
        return (
            session.query(cls.id).filter(cls.highest_education == education).first()[0]
        )


class FinalResult(Base):
    __tablename__ = "final_result"
    id = Column(Integer, primary_key=True, autoincrement=True)
    final_result = Column(String(11), nullable=False)

    @classmethod
    def seed_table(cls, session: Session):
        all_results = session.query(StudentInfo.final_result).distinct().all()
        session.add_all([cls(final_result=result[0]) for result in all_results])
        session.commit()

    @classmethod
    def get_id(cls, session: Session, result: str):
        return session.query(cls.id).filter(cls.final_result == result).first()[0]


class Student(Base):
    __tablename__ = "student"
    id = Column(Integer, primary_key=True, autoincrement=True)
    course_student_id = Column(Integer, nullable=False)
    course_id = Column(Integer, ForeignKey("course.id"), nullable=False)
    age_band_id = Column(Integer, ForeignKey("age_band.id"), nullable=False)
    imd_band_id = Column(Integer, ForeignKey("imd_band.id"), nullable=False)
    highest_education_id = Column(
        Integer, ForeignKey("highest_education.id"), nullable=False
    )
    region_id = Column(Integer, ForeignKey("region.id"), nullable=False)
    final_result_id = Column(Integer, ForeignKey("final_result.id"), nullable=False)
    is_female = Column(Integer)
    has_disability = Column(Integer)
    date_registration = Column(Integer)
    date_unregistration = Column(Integer)
    studied_credits = Column(Integer)
    num_of_prev_attempts = Column(Integer)

    @classmethod
    def from_student_info(cls, student_info: StudentInfo, session: Session):
        return cls(
            course_student_id=student_info.id_student,
            age_band_id=AgeBand.get_id(session, student_info.age_band),
            imd_band_id=ImdBand.get_id(session, student_info.imd_band),
            highest_education_id=HighestEducation.get_id(
                session, student_info.highest_education
            ),
            region_id=Region.get_id(session, student_info.region),
            final_result_id=FinalResult.get_id(session, student_info.final_result),
        )


class AssessmentType(Base):
    __tablename__ = "assessment_type"
    id = Column(Integer, primary_key=True, autoincrement=True)
    assessment_type = Column(String(4), nullable=False)


class Assessment(Base):
    __tablename__ = "assessment"
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("course.id"), nullable=False)
    assessment_type_id = Column(
        Integer, ForeignKey("assessment_type.id"), nullable=False
    )
    date = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)


class ActivityType(Base):
    __tablename__ = "activity_type"
    id = Column(Integer, primary_key=True, autoincrement=True)
    activity_type = Column(String(14), nullable=False)

    @classmethod
    def seed_table(cls, session: Session):
        all_activity_types = session.query(Vle.activity_type).distinct().all()
        session.add_all(
            [cls(activity_type=activity[0]) for activity in all_activity_types]
        )
        session.commit()


class VleCourseBridge(Base):
    __tablename__ = "vle_course_bridge"
    id = Column(Integer, primary_key=True, autoincrement=True)
    site_id = Column(Integer, nullable=False)
    course_id = Column(Integer, ForeignKey("course.id"), nullable=False)
    activity_type_id = Column(Integer, ForeignKey("activity_type.id"), nullable=False)
    week_from = Column(Integer)
    week_to = Column(Integer)


class StudentVleBridge(Base):
    __tablename__ = "student_vle_bridge"
    id = Column(Integer, primary_key=True, autoincrement=True)
    site_id = Column(Integer, ForeignKey("vle_course_bridge.site_id"))
    student_id = Column(Integer, ForeignKey("student.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("course.id"), nullable=False)
    date = Column(Integer, nullable=False)
    sum_click = Column(Integer, nullable=False)


class StudentAssessmentBridge(Base):
    __tablename__ = "student_assessment_bridge"
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("student.id"), nullable=False)
    assessment_id = Column(Integer, ForeignKey("assessment.id"), nullable=False)
    date_submitted = Column(Integer)
    is_banked = Column(Integer)
    score = Column(Float)
