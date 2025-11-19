from pydantic import BaseModel

class StudentCreate(BaseModel):
    name: str
    surname: str
    faculty: str
    curse: str
    score: float

class StudentUpdate(BaseModel):
    name: str | None = None
    surname: str | None = None
    faculty: str | None = None
    curse: str | None = None
    score: float | None = None

class StudentDelete(BaseModel):
    id: int
    name: str
    surname: str
    faculty: str
    curse: str
    score: float

    class Config:
        orm_mode = True
