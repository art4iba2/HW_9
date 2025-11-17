import csv
from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import sessionmaker, Session
from model import Student, Base

class Sudent_repository():
    def __init__(self, db_url="sqlite:///student.db"):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)

    def add_student(self, student: Student):
        with Session(self.engine) as session:
            session.add(student)
            session.commit()

    def get_all_students(self):
        with Session(self.engine) as session:
            return session.query(Student).all()

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

    def get_unique_curse(self, curse: str):
        with Session(self.engine) as session:
            return session.query(Student).filter(Student.curse == curse).all()

    def get_avg_score(self, faculty_name: str):
        with Session(self.engine) as session:
            stmt = select(func.avg(Student.score)).where(Student.faculty == faculty_name)
            result = session.execute(stmt).scalar()
            return float(result) if result else 0

repo = Sudent_repository()
repo.load_from_csv("students.csv")

print(repo.get_all_students())
print(repo.get_students_by_faculty("РЭФ"))
print(repo.get_unique_curse("Информатика"))
print(repo.get_avg_score("ФТФ"))