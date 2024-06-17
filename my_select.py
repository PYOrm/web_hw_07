from sqlalchemy import func, desc, create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from models import Student, Mark, Subject, Group, Teacher


def select_1(session: Session):
    res = session.query(Student.full_name, func.round(func.avg(Mark.mark), 2).label('avg_grade')) \
        .select_from(Mark).join(Student).group_by(Student.id).order_by(desc('avg_grade')).limit(5).all()
    return res


def select_2(session: Session):
    res = session.query(Student.full_name, Subject.subject_name, func.round(func.avg(Mark.mark), 2).label('avg_grade')) \
        .select_from(Mark).join(Student).join(Subject).group_by(Student.id, Subject.subject_name).order_by(
        Subject.subject_name, desc('avg_grade')).first()
    return res


def select_3(session: Session):
    res = session.query(Group.group_name, Subject.subject_name, func.round(func.avg(Mark.mark), 2).label('avg_grade')) \
        .select_from(Mark).join(Subject).join(Student).join(Group).group_by(Group.group_name,
                                                                            Subject.subject_name).having(
        Subject.subject_name == "Algebra").order_by(Subject.subject_name, desc('avg_grade')).all()
    return res


def select_4(session: Session):
    res = session.query(func.round(func.avg(Mark.mark), 2).label('avg_grade')) \
        .select_from(Mark).all()
    return res


def select_5(session: Session):
    res = session.query(Subject.subject_name) \
        .select_from(Subject).join(Teacher).where(Teacher.full_name == "Peter Blevins").all()
    return res


def select_6(session: Session):
    res = session.query(Group.group_name, Student.full_name) \
        .select_from(Student).join(Group).where(Group.group_name == "group_1").all()
    return res


def select_7(session: Session):
    res = session.query(Group.group_name, Subject.subject_name, Student.full_name, Mark.mark) \
        .select_from(Mark).join(Subject).join(Student).join(Group) \
        .where(Group.group_name == "group_1", Subject.subject_name == "Algebra").all()
    return res


def select_8(session: Session):
    res = session.query(Teacher.full_name, func.round(func.avg(Mark.mark), 2).label("avg")) \
        .select_from(Mark).join(Subject).join(Teacher) \
        .where(Teacher.full_name == "Peter Blevins").group_by(Teacher.full_name).all()
    return res


def select_9(session: Session):
    res = session.query(Subject.subject_name) \
        .select_from(Mark).join(Subject).join(Student) \
        .where(Student.full_name == "Eric White").distinct().all()
    return res


def select_10(session: Session):
    res = session.query(Subject.subject_name) \
        .select_from(Mark).join(Subject).join(Student).join(Teacher) \
        .where(Student.full_name == "Eric White", Teacher.full_name == "Peter Blevins").distinct().all()
    return res


def select_11(session: Session):
    res = session.query(func.round(func.avg(Mark.mark), 2).label("avg")) \
        .select_from(Mark).join(Subject).join(Student).join(Teacher) \
        .where(Student.full_name == "Eric White", Teacher.full_name == "Peter Blevins").one_or_none()
    return res


def select_12(session: Session):
    subjuery = session.query(func.max(func.DATE(Mark.timestamp)).label("lastdate")).select_from(Mark).join(Subject) \
        .join(Student).join(Group).where(Subject.subject_name == "Algebra", Group.group_name == "group_1") \
        .scalar_subquery()

    res = session.query(Student.full_name, Mark.mark, func.DATE(Mark.timestamp)) \
        .select_from(Mark).join(Subject).join(Student).join(Group) \
        .where(Group.group_name == "group_1", Subject.subject_name == "Algebra", func.DATE(Mark.timestamp) == subjuery) \
        .all()
    return res


# if __name__ == '__main__':
#     with open("db_conn_set.ini", "r", encoding="utf-8") as f:
#         db_conn_set = f.read()
#     engine = create_engine(db_conn_set, echo=False)
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     for r in select_12(session):
#         print(r)
