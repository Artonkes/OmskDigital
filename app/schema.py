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
    bio_min: str
    bio_max: str
    geo: str
    url_company: str
    contact: str
    type_company: str
    number: int
    off_name: str
    main_people: str
    # icon_company: str

    class Config:
        from_attributes  = True
