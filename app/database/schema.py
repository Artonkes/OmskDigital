from fastapi import Form, File, UploadFile
from pydantic import BaseModel

from typing import  Optional


class CompanySchema(BaseModel):
    name: str = Form(...)
    official_name: str = Form(...)
    bio_min: str = Form(...)
    bio_max: str = Form(...)
    keywords: str = Form(...)
    target: Optional[str] = Form(default=None)
    geo: str = Form(...)
    coordinates: str = Form(...)
    use_technology: str = Form(...)
    contact_number_phone: str = Form(...)
    contact_email: str = Form(...)
    contact_site: str = Form(...)
    contact_tg: Optional[str] = Form(default=None)
    contact_vk: Optional[str] = Form(default=None)
    founding_data: str = Form(...)

    icon: Optional[UploadFile] = File(...)
    photo_company: Optional[UploadFile] = File(None)

    class Config:
        from_attributes  = True

class ProjectCompanySchema(BaseModel):
    name_company: str  = Form(...)
    name_project: str = Form(...)
    project_photo: Optional[UploadFile] = File(None)

    class Config:
        from_attributes = True