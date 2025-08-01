import os
from typing import List
from sqlalchemy import select
from fastapi import HTTPException, APIRouter, UploadFile, File, Depends

from app.DataBase.database import SessionDepend
from app.schema import CollegeSchema, VacancySchema, CompanySchema, ContactShema
from app.DataBase.Model import CollegeModel, VacancyModel, CompanyModel
from app.DataBase.crud import setup_database, delete_setup, update_setup, upload_img, uploads_images

router = APIRouter(
    prefix="/method",
    tags=["AdminPanel"]
)

#DataBase
@router.post("/api/admin/create_table", summary="Create table")
async def create_table():
    await setup_database()
    return {"detail": "Table to create"}


#Company
@router.get("/api/admin/get_company", summary="Вывод всех компаний")
async def get_company(session: SessionDepend):
    try:
        query = select(
            CompanyModel.id,
            CompanyModel.name,
            CompanyModel.icon,
            CompanyModel.keywords,
            CompanyModel.bio_min
        )
        rows = await session.execute(query)
        result = rows.all()

        return [
            {
                "id": row.id,
                "name": row.name,
                "icon_company": row.icon,
                "keyword": row.keywords,
                "bio_min": row.bio_min
            }
            for row in result
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error is {e}")
    except HTTPException:
        raise HTTPException(status_code=404, detail=f"Error")

@router.get("/api/admin/get_company/{company_id}", summary="Вывод компании по id")
async def get_company_id(session: SessionDepend, company_id: int):
    try:
        query = select(
            CompanyModel.name,
            CompanyModel.icon,
            CompanyModel.target,
            CompanyModel.bio_min,
            CompanyModel.keywords,
            CompanyModel.bio_max,
            CompanyModel.geo,
            CompanyModel.contact,
            CompanyModel.official_name,
            CompanyModel.founding_data,
            CompanyModel.use_technology,
            CompanyModel.project,
            CompanyModel.project_photo,
            CompanyModel.photo_company
        ).where(CompanyModel.id == company_id)

        result = await session.execute(query)
        row = result.first()

        if row is None:
            raise HTTPException(status_code=404, detail="Company not found")

        row = row._mapping

        return [
            {
                "Minimum set for cards": {
                    "name": row["name"],
                    "target": row["target"],
                    "min_bio": row["bio_min"],
                    "icon": row["icon"],
                    "use_technology": row["use_technology"],
                    "contact": row["contact"],
                },
                "Maximum set for cards": {
                    "name": row["name"],
                    "icon": row["icon"],
                    "target": row["target"],
                    "keywords": row["keywords"].split(",") if row["keywords"] else None,
                    "min_bio": row["bio_min"],
                    "max_bio": row["bio_max"],
                    "contact": row["contact"],
                    "geo": row["geo"],
                    "official_name": row["official_name"],
                    "founding_data": row["founding_data"],
                    "project": {
                        "project_photo": row["project_photo"],
                        "project": row["project"]
                    },
                    "photo_company": row["photo_company"].split(",") if row["photo_company"] else None,
                }
            }
        ]

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Error while retrieving company data: {str(e)}")


@router.post("/api/admin/company/", summary="Добавление компаний")
async def add_company(session: SessionDepend, company: CompanySchema = Depends(),
                      icon: UploadFile = File(...),
                      photo_company: List[UploadFile] = File(...),
                      project_photo: UploadFile = File(...)):

    icon = await upload_img(file=icon,NameDIR="ICON" , NameSetup=company.name)
    photo_company = await uploads_images(file=photo_company,NameDIR="PHOTO COMPANY", NameSetup=company.name)
    project_photo = await upload_img(file=project_photo, NameDIR="PROJECT", NameSetup=company.name)

    new_company = CompanyModel(
        name=company.name,
        icon=icon,
        bio_min=company.bio_min,
        bio_max=company.bio_max,
        keywords=company.keywords,
        target=company.target,
        geo=company.geo,
        use_technology=company.use_technology,
        contact=company.contact,
        official_name=company.official_name,
        founding_data=company.founding_data,
        project=company.project,
        project_photo=project_photo,
        photo_company=photo_company,
        contact_tg=company.contact_tg,
        contact_vk=company.contact_vk
    )

    session.add(new_company)
    await session.commit()
    return {"detail": "Company appended"}


@router.put("/api/admin/update_company/{id_company}", summary="Обновление компании")
async def update_company(id_company: int, session: SessionDepend, company: CompanySchema = Depends(),
    icon: UploadFile = File(...),
    photo_company: List[UploadFile] = File(...),
    project_photo: UploadFile = File(...)
):
    try:
        icon = await upload_img(file=icon,NameDIR="ICON" , NameSetup=company.name)
        photo_company = await uploads_images(file=photo_company,NameDIR="PHOTO COMPANY", NameSetup=company.name)
        project_photo = await upload_img(file=project_photo, NameDIR="PROJECT", NameSetup=company.name)

        if icon:
            if company.icon and os.path.exists(company.icon):
                os.remove(f"app/Img Company/{company.name}/ICON/{company.icon}")
            company.icon = icon

        if photo_company:
            if company.photo_company and os.path.exists(company.photo_company):
                os.remove(f"app/Img Company/{company.name}/PHOTO COMPANY/{company.photo_company}")
            company.photo_company = photo_company

        if project_photo:
            if company.project_photo and os.path.exists(company.project_photo):
                os.remove(f"app/Img Company/{company.name}/PROJECT/{company.project_photo}")
            company.project_photo = project_photo

        await update_setup(id_setup=id_company, session=session, SetupModel=CompanyModel, setup_schema=company)
        return {"detail": "Company updated"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error is {e}")
    


@router.delete("/api/admin/delete_company/{id_company}", summary="Удаление компаний")
async def delete_company(id_company: int, session: SessionDepend):
    return await delete_setup(id_setup=id_company, session=session, SetupModel=CompanyModel)