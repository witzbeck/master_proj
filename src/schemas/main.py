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

from schemas.landing import Courses, StudentAssessment, StudentInfo, StudentVle, Vle

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
        all_courses = session.query(Courses).all()
        session.bulk_save_objects(
            [
                cls(
                    presentation_code=course.code_presentation,
                    start_year=course.start_year,
                    start_month=course.start_month,
                    start_date=course.start_date,
                )
                for course in all_courses
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
        all_courses = session.query(Courses).all()
        session.bulk_save_objects(
            [
                cls(
                    module_code=course.code_module,
                    domain=course.domain,
                    level=course.level,
                )
                for course in all_courses
            ]
        )


class Course(Base):
    __tablename__ = "course"
    id = Column(Integer, primary_key=True, autoincrement=True)
    module_id = Column(Integer, ForeignKey("module.id"), nullable=False)
    presentation_id = Column(Integer, ForeignKey("presentation.id"), nullable=False)
    course_length = Column(Integer, nullable=False)
    __table_args__ = (
        UniqueConstraint("module_id", "presentation_id", name="unique_course"),
    )

    @classmethod
    def from_course(cls, course: Courses, session: Session):
        return cls(
            module_id=session.query(Module.id)
            .filter(Module.module_code == course.code_module)
            .first()[0],
            presentation_id=session.query(Presentation.id)
            .filter(
                (Presentation.presentation_code == course.code_presentation)
                & (Presentation.start_year == course.start_year)
                & (Presentation.start_month == course.start_month)
                & (Presentation.start_date == course.start_date)
            )
            .first()[0],
            course_length=course.module_presentation_length,
        )

    @classmethod
    def seed_table(cls, session: Session):
        all_courses = session.query(Courses).all()
        session.bulk_save_objects(
            [cls.from_course(course, session) for course in all_courses]
        )
        session.commit()


class ImdBand(Base):
    __tablename__ = "imd_band"
    id = Column(Integer, primary_key=True, autoincrement=True)
    imd_band = Column(String(7), nullable=False)
    __table_args__ = (UniqueConstraint("imd_band", name="unique_imd_band"),)

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
    __table_args__ = (UniqueConstraint("age_band", name="unique_age_band"),)

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
    __table_args__ = (UniqueConstraint("region", name="unique_region"),)

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
    __table_args__ = (UniqueConstraint("highest_education", name="unique_education"),)

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
    __table_args__ = (UniqueConstraint("final_result", name="unique_final_result"),)

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
    __table_args__ = (
        UniqueConstraint("assessment_type", name="unique_assessment_type"),
    )

    @classmethod
    def seed_table(cls, session: Session):
        all_assessment_types = session.query(Vle.activity_type).distinct().all()
        session.add_all(
            [cls(assessment_type=activity[0]) for activity in all_assessment_types]
        )
        session.commit()


class Assessment(Base):
    __tablename__ = "assessment"
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("course.id"), nullable=False)
    assessment_type_id = Column(
        Integer, ForeignKey("assessment_type.id"), nullable=False
    )
    date = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    __table_args__ = (
        UniqueConstraint(
            "course_id", "assessment_type_id", "date", name="unique_assessment"
        ),
    )

    @classmethod
    def from_vle_course_bridge(cls, vle_course_bridge: Vle, session: Session):
        return cls(
            course_id=vle_course_bridge.course_id,
            assessment_type_id=session.query(AssessmentType.id)
            .filter(AssessmentType.assessment_type == vle_course_bridge.activity_type)
            .first()[0],
            date=vle_course_bridge.week_from,
            weight=0.0,
        )

    @classmethod
    def seed_table(cls, session: Session):
        all_vle_course_bridges = session.query(VleCourseBridge).all()
        session.bulk_save_objects(
            [
                cls.from_vle_course_bridge(vle_course_bridge, session)
                for vle_course_bridge in all_vle_course_bridges
            ]
        )
        session.commit()


class ActivityType(Base):
    __tablename__ = "activity_type"
    id = Column(Integer, primary_key=True, autoincrement=True)
    activity_type = Column(String(14), nullable=False)
    __table_args__ = (UniqueConstraint("activity_type", name="unique_activity_type"),)

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
    __table_args__ = (
        UniqueConstraint(
            "site_id", "course_id", "activity_type_id", name="unique_vle_course"
        ),
    )

    @classmethod
    def from_vle(cls, vle: Vle, session: Session):
        return cls(
            site_id=vle.id_site,
            course_id=session.query(Course.id)
            .filter(
                (
                    Course.module_id
                    == session.query(Module.id)
                    .filter(Module.module_code == vle.code_module)
                    .first()[0]
                )
                & (
                    Course.presentation_id
                    == session.query(Presentation.id)
                    .filter(
                        (Presentation.presentation_code == vle.code_presentation)
                        & (Presentation.start_year == vle.start_year)
                        & (Presentation.start_month == vle.start_month)
                        & (Presentation.start_date == vle.start_date)
                    )
                    .first()[0]
                )
            )
            .first()[0],
            activity_type_id=session.query(ActivityType.id)
            .filter(ActivityType.activity_type == vle.activity_type)
            .first()[0],
            week_from=vle.week_from,
            week_to=vle.week_to,
        )

    @classmethod
    def seed_table(cls, session: Session):
        all_vles = session.query(Vle).all()
        session.bulk_save_objects([cls.from_vle(vle, session) for vle in all_vles])
        session.commit()


class StudentVleBridge(Base):
    __tablename__ = "student_vle_bridge"
    id = Column(Integer, primary_key=True, autoincrement=True)
    site_id = Column(Integer, ForeignKey("vle_course_bridge.site_id"))
    student_id = Column(Integer, ForeignKey("student.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("course.id"), nullable=False)
    date = Column(Integer, nullable=False)
    sum_click = Column(Integer, nullable=False)

    @classmethod
    def from_student_vle(cls, student_vle: StudentVle, session: Session):
        return cls(
            site_id=session.query(VleCourseBridge.id)
            .filter(
                (VleCourseBridge.site_id == student_vle.site_id)
                & (VleCourseBridge.course_id == student_vle.course_id)
            )
            .first()[0],
            student_id=session.query(Student.id)
            .filter(Student.course_student_id == student_vle.student_id)
            .first()[0],
            course_id=student_vle.course_id,
            date=student_vle.date,
            sum_click=student_vle.sum_click,
        )

    @classmethod
    def seed_table(cls, session: Session):
        all_student_vles = session.query(StudentVle).all()
        session.bulk_save_objects(
            [
                cls.from_student_vle(student_vle, session)
                for student_vle in all_student_vles
            ]
        )
        session.commit()


class StudentAssessmentBridge(Base):
    __tablename__ = "student_assessment_bridge"
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("student.id"), nullable=False)
    assessment_id = Column(Integer, ForeignKey("assessment.id"), nullable=False)
    date_submitted = Column(Integer)
    is_banked = Column(Integer)
    score = Column(Float)

    @classmethod
    def from_student_assessment(
        cls, student_assessment: StudentAssessment, session: Session
    ):
        return cls(
            student_id=session.query(Student.id)
            .filter(Student.course_student_id == student_assessment.student_id)
            .first()[0],
            assessment_id=session.query(Assessment.id),
        )

    @classmethod
    def seed_table(cls, session: Session):
        all_student_assessments = session.query(StudentAssessment).all()
        session.bulk_save_objects(
            [
                cls.from_student_assessment(student_assessment, session)
                for student_assessment in all_student_assessments
            ]
        )
