from sqlalchemy.orm import declarative_base
from sqlalchemy import Integer, Column, String, Float, ForeignKey
Base = declarative_base()

class Student(Base):
    __tablename__ = 'student'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    faculty = Column(String)
    curse = Column(String)
    score = Column(Float)

    def __repr__(self):
        return (f"<student({self.id} name = {self.name} surname = {self.surname} "
                f"Faculty = {self.faculty} Curse = {self.curse}> Score = {self.score}>")
    

