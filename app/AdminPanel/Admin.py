from typing import List

from fastapi import HTTPException, APIRouter, UploadFile, File, Depends
from sqlalchemy import select, update


from app.DataBase.crud import setup_database, delete_setup, update_setup, upload_image
from app.DataBase.database import SessionDepend
from app.schema import CollegeSchema, VacancySchema, CompanySchema
from app.DataBase.Model import CollegeModel, VacancyModel, CompanyModel

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
            CompanyModel.url_company
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
async def add_company(session: SessionDepend, company: CompanySchema = Depends(), file: UploadFile = File(...)):
    icon_path = await upload_image(file=file, NameSetup=company.name)

    new_company = CompanyModel(
        name=company.name,
        bio_min=company.bio_min,
        bio_max=company.bio_max,
        geo=company.geo,
        icon_company=icon_path,
        url_company=company.url_company,
        contact=company.contact,
        type_company=company.type_company,
        use_technologists=company.url_company,
        number=company.number,
        off_name=company.off_name,
        main_people=company.main_people
    )

    session.add(new_company)
    await session.commit()
    return {"detail": "Company appended"}


@router.put("/api/admin/update_company/{id_company}", summary="Обновление компании", response_model=CompanySchema)
async def update_company(id_company: int, session: SessionDepend, company: CompanySchema = Depends(), file: UploadFile = File(...)):
    return await update_setup(
        id_setup=id_company,
        session=session,
        SetupModel=CompanyModel,
        setup_schema=company
    )


@router.delete("/api/admin/delete_company/{id_company}", summary="Удаление компаний")
async def delete_company(id_company: int, session: SessionDepend):
    return await delete_setup(id_setup=id_company, session=session, SetupModel=CompanyModel)


