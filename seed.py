import random
import faker
from faker.providers import DynamicProvider
import datetime
from sqlalchemy import create_engine
from models import Student, Subject, Teacher, Mark, Group
from sqlalchemy.orm import Session, sessionmaker


class FakeDataGenerator:
    subject_list = ['Mathematics', 'Algebra', 'Geometry', 'Science', 'Geography', 'History', 'English', 'Spanish',
                    'German', 'French', 'Latin', 'Greek', 'Arabic', 'Computer Science', 'Art', 'Economics', 'Music',
                    'Drama', 'Physical Education']

    def __init__(self, students_qty, teachers_qty, subjects_qty, marks_qty=20):
        self.session = None
        self.fk = faker.Faker()
        self.fk.add_provider(DynamicProvider(provider_name="subject", elements=self.subject_list))
        self.groups = self.records_groups()
        self.teachers = self.records_teacher(teachers_qty)
        self.subjects = self.records_subjects(subjects_qty)
        self.students = self.records_students(students_qty)
        self.marks = self.records_marks(marks_qty)

    def set_db_session(self, session: Session):
        self.session = session

    def gen_subjects(self, subjects_qty):
        res = set()
        while len(res) < subjects_qty:
            res.add(self.fk.subject())
        return list(res)

    def fill_db_with_fake_data(self):
        self.session.add_all(self.groups)
        self.session.commit()
        self.session.add_all(self.teachers)
        self.session.commit()
        self.session.add_all(self.subjects)
        self.session.commit()
        self.session.add_all(self.students)
        self.session.commit()
        self.session.add_all(self.marks)
        self.session.commit()

    def records_subjects(self, subjects_qty):
        subjects = self.gen_subjects(subjects_qty)
        ret = []
        for subj in subjects:
            ret.append(Subject(subj, random.choice(self.teachers)))
        return ret

    def records_groups(self):
        ret = []
        for group in range(1, 4):
            ret.append(Group(f"group_{group}"))
        return ret

    def records_teacher(self, teachers_qty):
        ret = []
        name = self.gen_names(teachers_qty)
        for teacher in name:
            ret.append(Teacher(teacher))
        return ret

    def records_students(self, students_qty):
        names = self.gen_names(students_qty)
        ret = []
        for student in names:
            ret.append(Student(student, random.choice(self.groups)))
        return ret

    def records_marks(self, marks_qty):
        ret = []
        for student in self.students:
            for _ in range(1, marks_qty + 1):
                ts = datetime.datetime(2024, random.randrange(1, 12),
                                       random.randrange(1, 28),
                                       random.randrange(1, 24),
                                       random.randrange(1, 60),
                                       random.randrange(1, 60))
                ret.append(Mark(student, random.choice(self.subjects), random.randrange(1, 100), ts))
        return ret

    def gen_names(self, qty: int) -> list:
        return [self.fk.name() for _ in range(1, qty + 1)]


if __name__ == "__main__":
    fk = FakeDataGenerator(50, 5, 8)
    with open("db_conn_set.ini", "r", encoding="utf-8") as f:
        db_conn_set = f.read()
    engine = create_engine(db_conn_set)
    Session = sessionmaker(bind=engine)
    session = Session()
    fk.set_db_session(session)
    fk.fill_db_with_fake_data()
