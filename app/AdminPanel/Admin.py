import base64
from typing import List
from sqlalchemy import select, update
from fastapi import HTTPException, APIRouter, UploadFile, File, Depends


from app.DataBase.database import SessionDepend
from app.schema import CollegeSchema, VacancySchema, CompanySchema
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
            CompanyModel.icon_company,
            CompanyModel.type_company,
            CompanyModel.number,
            CompanyModel.url_company
        )
        rows = await session.execute(query)
        result = rows.all()

        return [
            {
                "id": row.id,
                "name": row.name,
                "icon_company": row.icon_company,
                "type_company": row.type_company,
                "number": row.number,
                "url_company": row.url_company
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
            CompanyModel.icon_company,
            CompanyModel.type_company,
            CompanyModel.number,
            CompanyModel.url_company,

        ).where(CompanyModel.id == company_id)
        result = await session.execute(query)
        row = result.first()

        if row is None:
            raise HTTPException(status_code=404, detail=f"Is not found")

        return {
            "name": row.name,
            "icon_company": row.icon_company,
            "type_company": row.type_company,
            "number": row.number
        }

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Error to return: {str(e)}")

@router.post("/api/admin/company/", summary="Добавление компаний")
async def add_company(session: SessionDepend, company: CompanySchema = Depends(),
                      icon: UploadFile = File(...), photo_company: UploadFile = File(...), project_photo: UploadFile = File(...)):

    icon = await upload_img(file=icon,NameDIR="ICON" , NameSetup=company.name)
    photo_company = await upload_img(file=photo_company,NameDIR="PHOTO COMPANY", NameSetup=company.name)
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
        photo_company=photo_company
    )

    session.add(new_company)
    await session.commit()
    return {"detail": "Company appended"}


@router.put("/api/admin/update_company/{id_company}", summary="Обновление компании", response_model=CompanySchema)
async def update_company(id_company: int, session: SessionDepend, company: CompanySchema = Depends(),
                         icon: UploadFile = File(...), photo_company: UploadFile = File(...)):

    return await update_setup(
        id_setup=id_company,
        session=session,
        SetupModel=CompanyModel,
        setup_schema=company
    )


@router.delete("/api/admin/delete_company/{id_company}", summary="Удаление компаний")
async def delete_company(id_company: int, session: SessionDepend):
    return await delete_setup(id_setup=id_company, session=session, SetupModel=CompanyModel)


