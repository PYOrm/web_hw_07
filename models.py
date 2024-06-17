import datetime

from sqlalchemy.orm import declarative_base, mapped_column, Mapped, relationship
from sqlalchemy import Column, Integer, ForeignKey, String

Base = declarative_base()


class Group(Base):
    __tablename__ = "groups"
    id: Mapped[int] = mapped_column(nullable=False, primary_key=True, autoincrement=True)
    group_name: Mapped[str] = mapped_column(String(30), nullable=False)
    student: Mapped["Student"] = relationship("Student", back_populates="group")

    def __init__(self, group_name):
        self.group_name = group_name


class Teacher(Base):
    __tablename__ = "teachers"
    id: Mapped[int] = mapped_column(nullable=False, primary_key=True, autoincrement=True)
    full_name: Mapped[str] = Column(String(50), nullable=False)
    subject: Mapped["Subject"] = relationship("Subject", back_populates="teacher")

    def __init__(self, name):
        self.full_name = name


class Student(Base):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(nullable=False, autoincrement=True, primary_key=True)
    full_name: Mapped[str] = mapped_column(nullable=False, type_=String(50))
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    group: Mapped["Group"] = relationship(Group, back_populates="student")
    mark: Mapped["Mark"] = relationship("Mark", back_populates="student")

    def __init__(self, name, group=None):
        self.full_name = name
        self.group = group


class Subject(Base):
    __tablename__ = "subjects"
    id: Mapped[int] = mapped_column(autoincrement=True, nullable=False, primary_key=True)
    subject_name: Mapped[str] = mapped_column(nullable=False)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id"))
    teacher: Mapped["Teacher"] = relationship(Teacher, back_populates="subject")
    mark: Mapped["Mark"] = relationship("Mark", back_populates="subject")

    def __init__(self, name, teacher=None):
        self.subject_name = name
        self.teacher = teacher


class Mark(Base):
    __tablename__ = "marks"
    id: Mapped[int] = mapped_column(nullable=False, autoincrement=True, primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), nullable=False)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"), nullable=False)
    mark: Mapped[int] = mapped_column(nullable=False)
    timestamp: Mapped[datetime.datetime] = mapped_column(default="CURRENT_TIMESTAMP", nullable=False)
    student: Mapped[Student] = relationship(Student, back_populates="mark")
    subject: Mapped[Subject] = relationship(Subject, back_populates="mark")

    def __init__(self, student: Student, subject: Subject, mark, timestamp):
        self.student = student
        self.subject = subject
        self.mark = mark
        self.timestamp = timestamp
