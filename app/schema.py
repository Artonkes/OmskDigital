from pydantic import BaseModel
from typing import List, Optional
from fastapi import Form

class ContactShema(BaseModel):
    NumberPhone: str = Form(...)
    email: str = Form(...)
    vk: str = Form(...)
    tg: str = Form(...)

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
    bio_min: str = Form(...)
    bio_max: str = Form(...)
    keywords: str = Form(...)
    target: str = Form(...)
    geo: str = Form(...)
    use_technology: str = Form(...)
    contact: str = Form(...)
    contact_tg: Optional[str] = Form(default=None)
    contact_vk: Optional[str] = Form(default=None)
    official_name: str = Form(...)
    founding_data: str = Form(...)
    project: str = Form(...)

    icon: Optional[str] = None
    photo_company: Optional[str] = None
    project_photo: Optional[str] = None

    class Config:
        from_attributes  = True
