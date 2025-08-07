import os
from typing import List, Optional

from sqlalchemy import select
from fastapi import HTTPException, APIRouter, UploadFile, File, Depends

from app.DataBase.database import SessionDepend
from app.schema import CompanySchema, ProjectCompanySchema
from app.DataBase.Model import CompanyModel, ProjectCompanyModel
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
@router.get("/api/admin/get_company", summary="Get all companies")
async def get_company(session: SessionDepend):
    try:
        query = select(
            CompanyModel.id,
            CompanyModel.name,
            CompanyModel.icon,
            CompanyModel.keywords,
            CompanyModel.bio_min,
        )
        rows = await session.execute(query)
        result = rows.all()

        return [
            {
                "id": row.id,
                "name": row.name,
                "icon_company": row.icon,
                "keyword": row.keywords.split(",") if row.keywords else None,
                "bio_min": row.bio_min
            }
            for row in result
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error is {e}")
    except HTTPException:
        raise HTTPException(status_code=404, detail=f"Error")


@router.get("/api/admin/get_company/{company_id}", summary="Get company by id")
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
            CompanyModel.contact_number_phone,
            CompanyModel.contact_email,
            CompanyModel.contact_site,
            CompanyModel.contact_tg,
            CompanyModel.contact_vk,
            CompanyModel.official_name,
            CompanyModel.founding_data,
            CompanyModel.use_technology,
            CompanyModel.photo_company
        ).where(CompanyModel.id == company_id)

        result = await session.execute(query)
        row = result.first()

        if row is None:
            raise HTTPException(status_code=404, detail="Company not found")

        row = row._mapping

        project_query = select(
            ProjectCompanyModel.id,
            ProjectCompanyModel.name_project,
            ProjectCompanyModel.photo,
        ).where(ProjectCompanyModel.id_company == company_id)

        project_result = await session.execute(project_query)
        project_rows = project_result.all()

        projects = []
        if project_rows:
            projects = [
                {
                    "id": proj.id,
                    "name_project": proj.name_project,
                    "photo": proj.photo
                }
                for proj in project_rows
            ]

        return {
            "Minimum set for cards": {
                "name": row["name"],
                "target": row["target"],
                "min_bio": row["bio_min"],
                "icon": row["icon"],
                "use_technology": row["use_technology"].split(",") if row["keywords"] else None,
                "number_phone": row["contact_number_phone"],
                "vk": row["contact_vk"],
                "tg": row["contact_tg"],
            },
            "Maximum set for cards": {
                "name": row["name"],
                "icon": row["icon"],
                "target": row["target"],
                "keywords": row["keywords"].split(",") if row["keywords"] else None,
                "min_bio": row["bio_min"],
                "max_bio": row["bio_max"],
                "number_phone": row["contact_number_phone"],
                "email": row["contact_email"],
                "site": row["contact_site"],
                "vk": row["contact_vk"],
                "tg": row["contact_tg"],
                "geo": row["geo"],
                "official_name": row["official_name"],
                "founding_data": row["founding_data"],
                "projects": projects,
                "photo_company": row["photo_company"],
            }
        }

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Error while retrieving company data: {str(e)}")

@router.post("/api/admin/company/", summary="Adding a company")
async def add_company(session: SessionDepend, company: CompanySchema = Depends(),
        icon: UploadFile = File(...), photo_company: List[UploadFile] = File(...)):
    try:
        if icon:
            icon = await upload_img(file=icon, NameDIR="ICON", NameSetup=company.name)
        else:
            icon = None
        if photo_company:
            photo_company = await uploads_images(file=photo_company, NameDIR="PHOTO COMPANY", NameSetup=company.name)
        else:
            photo_company = None

        new_company = CompanyModel(
            name=company.name,
            icon=icon,
            bio_min=company.bio_min,
            bio_max=company.bio_max,
            keywords=company.keywords,
            target=company.target,
            geo=company.geo,
            use_technology=company.use_technology,
            contact_number_phone=company.contact_number_phone,
            contact_email=company.contact_email,
            contact_site=company.contact_site,
            contact_tg=company.contact_tg,
            contact_vk=company.contact_vk,
            official_name=company.official_name,
            founding_data=company.founding_data,
            photo_company=photo_company,

        )

        session.add(new_company)
        await session.commit()
        return {"detail": "Company adding"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error is: {e}")


@router.post("/api/admin/company/project/")
async def adding_project(session: SessionDepend, project: ProjectCompanySchema = Depends(), project_photo: Optional[UploadFile] = File(default=None)):
    try:
        company_query = select(CompanyModel).where(CompanyModel.name == project.name_company)
        company_result = await session.execute(company_query)
        company = company_result.scalar_one_or_none()
        
        if company is None:
            raise HTTPException(status_code=404, detail="Company not found")

        if project_photo:
            project_photo = await upload_img(file=project_photo, NameDIR="PROJECT", NameSetup=project.name_company)
        else:
            project_photo = None

        new_project = ProjectCompanyModel(
            id_company=company.id,
            name_project=project.name_project,
            photo=project_photo,
        )

        session.add(new_project)
        await session.commit()

        return {"detail": "Project adding"}

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Error is: {e}")


@router.put("/api/admin/update_company/{id_company}", summary="Update company")
async def update_company(id_company: int, session: SessionDepend, company: CompanySchema = Depends(),
    icon: UploadFile = File(...),
    photo_company: Optional[List[UploadFile]] = File(default=None),
):
    try:
        icon = await upload_img(file=icon,NameDIR="ICON" , NameSetup=company.name)
        photo_company = await uploads_images(file=photo_company,NameDIR="PHOTO COMPANY", NameSetup=company.name)

        if icon:
            if company.icon and os.path.exists(company.icon):
                os.remove(f"app/Img Company/{company.name}/ICON/{company.icon}")
            company.icon = icon


        if photo_company:
            if company.photo_company and os.path.exists(company.photo_company):
                os.remove(f"app/Img Company/{company.name}/PHOTO COMPANY/{company.photo_company}")
            company.photo_company = photo_company
        else:
            pass

        await update_setup(id_setup=id_company, session=session, SetupModel=CompanyModel, setup_schema=company)

        return {"detail": "Company updated"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error is: {e}")


@router.put("/api/admin/update_company/project/{id_project}", summary="Update project company")
async def update_project(id_project: int, session: SessionDepend, project: ProjectCompanySchema = Depends(),
    project_photo: Optional[UploadFile] = File(default=None)):
    try:
        project_photo = await upload_img(file=project_photo, NameDIR="PROJECT", NameSetup=project.name_company)

        if project_photo:
            if project.photo and os.path.exists(project.photo):
                os.remove(f"app/Img Company/{project.name_company}/PROJECT/{project.photo}")
            project.photo = project_photo
        else:
            pass
        
        await update_setup(id_setup=id_project, session=session, SetupModel=ProjectCompanyModel, setup_schema=project)


        return {"detail": "Project updated"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error is: {e}")


@router.delete("/api/admin/delete_company/{id_company}", summary="Delete to company")
async def delete_company(id_company: int, session: SessionDepend):
    try:
        await delete_setup(id_setup=id_company, session=session, SetupModel=CompanyModel)
        await session.commit()
        return {"detail": "Company deleted"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error is: {e}")