# app/models.py
from __future__ import annotations

from datetime import datetime
from typing import List

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    SmallInteger,
    String,
    UniqueConstraint,
    CheckConstraint,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    students: Mapped[List["Student"]] = relationship(
        back_populates="group",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Group id={self.id} name={self.name!r}>"


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)

    group_id: Mapped[int] = mapped_column(
        ForeignKey("groups.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    group: Mapped["Group"] = relationship(back_populates="students")

    grades: Mapped[List["Grade"]] = relationship(
        back_populates="student",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Student id={self.id} full_name={self.full_name!r} group_id={self.group_id}>"


class Teacher(Base):
    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)

    subjects: Mapped[List["Subject"]] = relationship(
        back_populates="teacher",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Teacher id={self.id} full_name={self.full_name!r}>"


class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)

    teacher_id: Mapped[int] = mapped_column(
        ForeignKey("teachers.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    teacher: Mapped["Teacher"] = relationship(back_populates="subjects")

    grades: Mapped[List["Grade"]] = relationship(
        back_populates="subject",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        UniqueConstraint("teacher_id", "name", name="uq_subject_teacher_name"),
    )

    def __repr__(self) -> str:
        return f"<Subject id={self.id} name={self.name!r} teacher_id={self.teacher_id}>"


class Grade(Base):
    __tablename__ = "grades"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    subject_id: Mapped[int] = mapped_column(
        ForeignKey("subjects.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    value: Mapped[int] = mapped_column(SmallInteger, nullable=False)

    received_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    student: Mapped["Student"] = relationship(back_populates="grades")
    subject: Mapped["Subject"] = relationship(back_populates="grades")

    __table_args__ = (
        CheckConstraint("value >= 1 AND value <= 12", name="ck_grade_value_range"),
    )

    def __repr__(self) -> str:
        return (
            f"<Grade id={self.id} student_id={self.student_id} "
            f"subject_id={self.subject_id} value={self.value} received_at={self.received_at}>"
        )
