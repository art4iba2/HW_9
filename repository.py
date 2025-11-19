import csv
from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import Session
from model import Student, Base

class Sudent_repository():
    def __init__(self, db_url="sqlite:///student.db"):
        self.engine = create_engine(db_url, echo=True)
        Base.metadata.create_all(self.engine)

    #CREATE
    def add_student(self, student: Student):
        with Session(self.engine) as session:
            session.add(student)
            session.commit()

    #READ
    def get_all_students(self):
        with Session(self.engine) as session:
            return session.query(Student).all()

    #UPDATE
    def update_student(self, student_id: int, **kwargs):
        with Session(self.engine) as session:
            student = session.get(Student, student_id)
            if not student:
                return None
            for key, value in kwargs.items():
                setattr(student, key, value)
            session.commit()
            return student

    #DELETE
    def delete_student(self, student_id: int):
        with Session(self.engine) as session:
            student = session.get(Student, student_id)
            if not student:
                return False
            session.delete(student)
            session.commit()
            return True



    def load_from_csv(self, file_patch: str):
        with Session(self.engine) as session:
            with open(file_patch, encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    student = Student(
                        surname = row["Фамилия"],
                        name = row["Имя"],
                        faculty = row["Факультет"],
                        curse = row["Курс"],
                        score = row["Оценка"]
                    )
                    session.add(student)
            session.commit()

    def get_students_by_faculty(self, faculty: str):
        with Session(self.engine) as session:
            return session.query(Student).filter(Student.faculty == faculty).all()

    def get_unique_curse(self):
        with Session(self.engine) as session:
            stmt = select(Student.curse).distinct()
            return [row for row, in session.execute(stmt)]

    def get_avg_score(self, faculty_name: str):
        with Session(self.engine) as session:
            stmt = select(func.avg(Student.score)).where(Student.faculty == faculty_name)
            result = session.execute(stmt).scalar()
            return float(result) if result else 0

    def get_students_under_30(self, curse: str):
        with Session(self.engine) as session:
            stmt = select(Student).where(Student.curse == curse, Student.score < 30).order_by(Student.score.desc())
            result = session.execute(stmt).all()
            return f"{list(result)} \n {len(result)}"

    def drop_db(self):
        Base.metadata.drop_all(bind=self.engine)


repo = Sudent_repository()
repo.load_from_csv("students.csv")


print(repo.get_unique_curse())
print(repo.get_students_under_30("Информатика"))
