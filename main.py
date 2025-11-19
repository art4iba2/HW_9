import uvicorn
from fastapi import FastAPI, HTTPException
from repository import Sudent_repository
from model import Student
from schemas import StudentCreate, StudentUpdate, StudentDelete

app = FastAPI(title="Student Management API")
repo = Sudent_repository()

#CREATE
@app.post("/students")
async def create_student(student: StudentCreate):
    student = Student(**student.model_dump())
    repo.add_student(student)
    return student


#READ_ALL
@app.get("/students")
def read_students():
    return repo.get_all_students()


#READ_ONE
@app.get("/students/{student_id}")
def read_student(student_id: int):
    student = repo.get_student(student_id)
    return student


#UPDATE
@app.put("/students/{student_id}")
def update_student(student_id: int, student: StudentUpdate):
    updated_student = repo.update_student(student_id, **student.model_dump())
    if not updated_student:
        raise HTTPException(status_code=404, detail="Student not found")
    return updated_student

#DELETE
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    deleted = repo.delete_student(student_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Student not found")
    return deleted


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
