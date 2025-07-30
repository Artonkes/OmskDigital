from pydantic import BaseModel
from typing import List
from fastapi import Form

class ContactShema(BaseModel):
    NumberPhone: str
    email: str
    vk: str
    tg: str

class CollegeSchema(BaseModel):
    name: str
    bio: str | None
    training_time: int | None

class VacancySchema(BaseModel):
    name: str
    bio: str
    salary: int
    city: int
    company_name: str

class CompanySchema(BaseModel):
    name: str = Form(...)
    # icon: str = Form(...)
    bio_min: str = Form(...)
    bio_max: str = Form(...)
    keywords: str = Form(...)
    target: str = Form(...)
    geo: str = Form(...)
    use_technology: str = Form(...)
    contact: List[ContactShema] = Form(...)
    official_name: str = Form(...)
    founding_data: str = Form(...)
    project: str = Form(...)
    # photo_company: str = Form(...)

    class Config:
        from_attributes  = True
