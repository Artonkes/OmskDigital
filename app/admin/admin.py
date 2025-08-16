import os

from sqlalchemy import select
from fastapi import HTTPException, APIRouter, UploadFile, File, Depends

from app.exeptions import handle_error_500
from app.database.schema import CompanySchema, ProjectCompanySchema
from app.config import return_path_file_company
from app.database.database import SessionDepend
from app.database.model import CompanyModel, ProjectCompanyModel
from app.database.crud import delete_setup, update_setup, upload_img, uploads_images

router = APIRouter(
    prefix="/method",
    tags=["admin"]
)

# Company
@handle_error_500
@router.get("/api/admin/get_company", summary="Get all companies")
async def get_company(session: SessionDepend):
    query = select(
        CompanyModel.id,
        CompanyModel.name,
        CompanyModel.icon,
        CompanyModel.keywords,
        CompanyModel.bio_min,
        CompanyModel.coordinates,
        CompanyModel.geo,
    )
    rows = await session.execute(query)
    result = rows.all()

    return [
        {
            "id": row.id,
            "name": row.name,
            #TODO
            # "icon": "http://127.0.0.1:8000/media" + row.icon
            "icon": row.icon,
            "keyword": row.keywords.split(",") if row.keywords else None,
            "bio_min": row.bio_min,
            "coordinates": row.coordinates,
            "geo": row.geo,
        }
        for row in result
    ]

@handle_error_500
@router.get("/api/admin/get_company/{company_id}", summary="Get company by id")
async def get_company_id(session: SessionDepend, company_id: int):

    query = select(
        CompanyModel.name,
        CompanyModel.icon,
        CompanyModel.target,
        CompanyModel.bio_min,
        CompanyModel.keywords,
        CompanyModel.bio_max,
        CompanyModel.geo,
        CompanyModel.coordinates,
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

    projects = [
        {
            "id": proj.id,
            "name_project": proj.name_project,
            "photo": proj.photo
        }
        for proj in project_rows
    ] if project_rows else []

    return {
        "Minimum set for cards": {
            "name": row["name"],
            "target": row["target"],
            "min_bio": row["bio_min"],
            "icon": row["icon"],
            "use_technology": row["use_technology"].split(",") if row["use_technology"] else None,
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
            "coordinates": row["coordinates"],
            "official_name": row["official_name"],
            "founding_data": row["founding_data"],
            "projects": projects,
            "photo_company": row["photo_company"],
        }
    }


@handle_error_500
@router.post("/api/admin/company/", summary="Adding a company")
async def add_company(session: SessionDepend, company: CompanySchema = Depends()):

    if company.icon:
        company.icon = await upload_img(file=company.icon, NameDIR="ICON", NameSetup=company.name)

    if company.photo_company:
        company.photo_company = await uploads_images(file=company.photo_company, NameDIR="PHOTO COMPANY", NameSetup=company.name)

    new_company = CompanyModel(
        name=company.name,
        icon=company.icon,
        bio_min=company.bio_min,
        bio_max=company.bio_max,
        keywords=company.keywords,
        target=company.target,
        geo=company.geo,
        coordinates=company.coordinates,
        use_technology=company.use_technology,
        contact_number_phone=company.contact_number_phone,
        contact_email=company.contact_email,
        contact_site=company.contact_site,
        contact_tg=company.contact_tg,
        contact_vk=company.contact_vk,
        official_name=company.official_name,
        founding_data=company.founding_data,
        photo_company=company.photo_company,
    )

    session.add(new_company)
    await session.commit()
    return {"detail": "Company adding"}


@handle_error_500
@router.post("/api/admin/company/project/")
async def adding_project(session: SessionDepend, project: ProjectCompanySchema = Depends()):
    company_query = select(CompanyModel).where(CompanyModel.name == project.name_company)
    company_result = await session.execute(company_query)
    company = company_result.scalar_one_or_none()

    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")

    if project.project_photo:
        project.project_photo = await upload_img(file=project.project_photo, NameDIR="PROJECT", NameSetup=project.name_company)

    new_project = ProjectCompanyModel(
        id_company=company.id,
        name_project=project.name_project,
        photo=project.project_photo,
    )

    session.add(new_project)
    await session.commit()

    return {"detail": "Project adding"}


@handle_error_500
@router.put("/api/admin/update_company/{id_company}", summary="Update company")
async def update_company(id_company: int, session: SessionDepend, company: CompanySchema = Depends()):

    company.icon = await upload_img(file=company.icon, NameDIR="ICON", NameSetup=company.name)
    photo_company = await uploads_images(file=company.photo_company, NameDIR="PHOTO COMPANY", NameSetup=company.name)

    if company.icon:
        if company.icon and os.path.exists(return_path_file_company(name_company=company.name, photo=company.photo_company)):
            os.remove(return_path_file_company(name_company=company.name, photo=company.photo_company))
        company.icon = company.icon

    if photo_company:
        if company.photo_company and os.path.exists(return_path_file_company(name_company=company.name, photo=company.photo_company)):
            os.remove(f"app/Img Company/{company.name}/PHOTO COMPANY/{company.photo_company}")
        company.photo_company = photo_company

    await update_setup(id_setup=id_company, session=session, SetupModel=CompanyModel, setup_schema=company)

    return {"detail": "Company updated"}


@handle_error_500
@router.put("/api/admin/update_company/project/{id_project}", summary="Update project company")
async def update_project(id_project: int, session: SessionDepend, project: ProjectCompanySchema = Depends()):
    if project.project_photo:
        if project.project_photo and os.path.exists(return_path_file_company(name_company=project.name_company, photo=project.project_photo)):
            os.remove(return_path_file_company(name_company=project.name_company, photo=project.project_photo))
        project.project_photo = project.project_photo

    await update_setup(id_setup=id_project, session=session, SetupModel=ProjectCompanyModel, setup_schema=project)
    a = 1/0
    return {"detail": "Project updated"}


@handle_error_500
@router.delete("/api/admin/delete_company/{id_company}", summary="Delete to company")
async def delete_company(id_company: int, session: SessionDepend):
    await delete_setup(id_setup=id_company, session=session, SetupModel=CompanyModel)
    await session.commit()
    return {"detail": "Company deleted"}
