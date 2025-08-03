from fastapi import Form
from pydantic import BaseModel

from typing import  Optional


class CompanySchema(BaseModel):
    name: str = Form(...)
    bio_min: str = Form(...)
    bio_max: str = Form(...)
    keywords: str = Form(...)
    target: str = Form(...)
    geo: str = Form(...)
    use_technology: str = Form(...)
    contact: str = Form(...)
    official_name: str = Form(...)
    founding_data: str = Form(...)
    contact_tg: Optional[str] = Form(default=None)
    contact_vk: Optional[str] = Form(default=None)

    class Config:
        from_attributes  = True

class ProjectCompanySchema(BaseModel):
    id_company: int = Form(...)
    name_company: str  = Form(...)
    name_project: str = Form(...)
    photo: str = Form(...)

    class Config:
        from_attributes = True