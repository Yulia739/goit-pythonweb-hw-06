from __future__ import annotations

from typing import List, Tuple

from sqlalchemy import func, desc
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models import Student, Group, Teacher, Subject, Grade


# 1) Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
def select_1(session: Session) -> List[Tuple[int, str, float]]:
    rows = (
        session.query(
            Student.id,
            Student.full_name,
            func.avg(Grade.value).label("avg_grade"),
        )
        .join(Grade, Grade.student_id == Student.id)
        .group_by(Student.id, Student.full_name)
        .order_by(desc("avg_grade"))
        .limit(5)
        .all()
    )
    return [(sid, name, float(avg)) for sid, name, avg in rows]


# 2) Знайти студента із найвищим середнім балом з певного предмета.
def select_2(session: Session, subject_id: int) -> Tuple[int, str, float] | None:
    row = (
        session.query(
            Student.id,
            Student.full_name,
            func.avg(Grade.value).label("avg_grade"),
        )
        .join(Grade, Grade.student_id == Student.id)
        .filter(Grade.subject_id == subject_id)
        .group_by(Student.id, Student.full_name)
        .order_by(desc("avg_grade"))
        .limit(1)
        .one_or_none()
    )
    if not row:
        return None
    sid, name, avg = row
    return (sid, name, float(avg))


# 3) Знайти середній бал у групах з певного предмета.
def select_3(session: Session, subject_id: int) -> List[Tuple[int, str, float]]:
    rows = (
        session.query(
            Group.id,
            Group.name,
            func.avg(Grade.value).label("avg_grade"),
        )
        .join(Student, Student.group_id == Group.id)
        .join(Grade, Grade.student_id == Student.id)
        .filter(Grade.subject_id == subject_id)
        .group_by(Group.id, Group.name)
        .order_by(Group.name)
        .all()
    )
    return [(gid, gname, float(avg)) for gid, gname, avg in rows]


# 4) Знайти середній бал на потоці (по всій таблиці оцінок).
def select_4(session: Session) -> float | None:
    avg_val = session.query(func.avg(Grade.value)).scalar()
    return float(avg_val) if avg_val is not None else None


# 5) Знайти які курси читає певний викладач.
def select_5(session: Session, teacher_id: int) -> List[Tuple[int, str]]:
    rows = (
        session.query(Subject.id, Subject.name)
        .filter(Subject.teacher_id == teacher_id)
        .order_by(Subject.name)
        .all()
    )
    return [(sid, name) for sid, name in rows]


# 6) Знайти список студентів у певній групі.
def select_6(session: Session, group_id: int) -> List[Tuple[int, str]]:
    rows = (
        session.query(Student.id, Student.full_name)
        .filter(Student.group_id == group_id)
        .order_by(Student.full_name)
        .all()
    )
    return [(sid, name) for sid, name in rows]


# 7) Знайти оцінки студентів у окремій групі з певного предмета.
def select_7(session: Session, group_id: int, subject_id: int) -> List[Tuple[int, str, int]]:
    rows = (
        session.query(
            Student.id,
            Student.full_name,
            Grade.value,
        )
        .join(Grade, Grade.student_id == Student.id)
        .filter(Student.group_id == group_id, Grade.subject_id == subject_id)
        .order_by(Student.full_name, Grade.received_at)
        .all()
    )
    return [(sid, name, int(val)) for sid, name, val in rows]


# 8) Знайти середній бал, який ставить певний викладач зі своїх предметів.
def select_8(session: Session, teacher_id: int) -> float | None:
    avg_val = (
        session.query(func.avg(Grade.value))
        .join(Subject, Subject.id == Grade.subject_id)
        .filter(Subject.teacher_id == teacher_id)
        .scalar()
    )
    return float(avg_val) if avg_val is not None else None


# 9) Знайти список курсів, які відвідує певний студент.
def select_9(session: Session, student_id: int) -> List[Tuple[int, str]]:
    rows = (
        session.query(Subject.id, Subject.name)
        .join(Grade, Grade.subject_id == Subject.id)
        .filter(Grade.student_id == student_id)
        .distinct()
        .order_by(Subject.name)
        .all()
    )
    return [(sid, name) for sid, name in rows]


# 10) Список курсів, які певному студенту читає певний викладач.
def select_10(session: Session, student_id: int, teacher_id: int) -> List[Tuple[int, str]]:
    rows = (
        session.query(Subject.id, Subject.name)
        .join(Grade, Grade.subject_id == Subject.id)
        .filter(Grade.student_id == student_id, Subject.teacher_id == teacher_id)
        .distinct()
        .order_by(Subject.name)
        .all()
    )
    return [(sid, name) for sid, name in rows]


if __name__ == "__main__":
    with SessionLocal() as session:
        print("select_1:", select_1(session))
        print("select_4:", select_4(session))
