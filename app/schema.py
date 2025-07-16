from pydantic import BaseModel
from typing import List

class DirectionSchema(BaseModel):
    DirectionName: str

    class Config:
        from_attributes = True

class CollegeSchema(BaseModel):
    name: str
    bio: str | None
    training_time: int | None
    directions: List[DirectionSchema]

    class Config:
        from_attributes = True

class VacancySchema(BaseModel):
    name: str
    bio: str
    salary: int
    city: int
    company_name: str

class CompanySchema(BaseModel):
    name: str
    target: str
    logo: str
    contacts: str
    type_company: str
    quantity: int
