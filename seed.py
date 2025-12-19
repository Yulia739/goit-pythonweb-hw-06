import random
from datetime import datetime, timedelta

from faker import Faker
from sqlalchemy import delete
from sqlalchemy.orm import Session

from app.db import SessionLocal  # :contentReference[oaicite:2]{index=2}
from app.models import Group, Student, Teacher, Subject, Grade  # :contentReference[oaicite:3]{index=3}


fake = Faker("uk_UA")


def seed_db() -> None:
    GROUPS_COUNT = 3
    STUDENTS_COUNT = random.randint(30, 50)
    TEACHERS_COUNT = random.randint(3, 5)
    SUBJECTS_COUNT = random.randint(5, 8)

    with SessionLocal() as session:

        session.execute(delete(Grade))
        session.execute(delete(Student))
        session.execute(delete(Subject))
        session.execute(delete(Teacher))
        session.execute(delete(Group))
        session.commit()


        groups = []
        for i in range(1, GROUPS_COUNT + 1):
            g = Group(name=f"Group-{i}")
            session.add(g)
            groups.append(g)
        session.commit()


        teachers = []
        for _ in range(TEACHERS_COUNT):
            t = Teacher(full_name=fake.name())
            session.add(t)
            teachers.append(t)
        session.commit()

        used_subject_names = set()
        subjects = []
        while len(subjects) < SUBJECTS_COUNT:
            name = fake.job()[:110]
            if name in used_subject_names:
                continue
            used_subject_names.add(name)
            s = Subject(name=name, teacher=random.choice(teachers))
            session.add(s)
            subjects.append(s)
        session.commit()


        students = []
        for _ in range(STUDENTS_COUNT):
            st = Student(full_name=fake.name(), group=random.choice(groups))
            session.add(st)
            students.append(st)
        session.commit()

        now = datetime.now()
        for st in students:
            grades_count = random.randint(10, 20)
            for _ in range(grades_count):
                subj = random.choice(subjects)
                value = random.randint(1, 12)
                received_at = now - timedelta(days=random.randint(0, 180), hours=random.randint(0, 23))

                session.add(
                    Grade(
                        student_id=st.id,
                        subject_id=subj.id,
                        value=value,
                        received_at=received_at,
                    )
                )

        session.commit()

    print(
        f"Seed complete: groups={GROUPS_COUNT}, students={STUDENTS_COUNT}, "
        f"teachers={TEACHERS_COUNT}, subjects={SUBJECTS_COUNT}"
    )


if __name__ == "__main__":
    seed_db()
