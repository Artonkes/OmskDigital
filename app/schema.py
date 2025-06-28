from pydantic import BaseModel

class CollegeShema(BaseModel):
    name: str
    bio: str
    max_ball: int
    min_ball: int
    paid_places: int
    free_places: int

class VacancyShema(BaseModel):
    name: str
    bio: str
    work_experience: int
    schedule: str
    work_format: str
    salary: int
    city: int