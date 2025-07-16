from fastapi import HTTPException, APIRouter

from sqlalchemy import select, update


from app.DataBase.crud import setup_database, delete_setup, get_setup, update_setup
from app.DataBase.database import SessionDepend
from app.schema import CollegeSchema, VacancySchema, CompanySchema
from app.DataBase.Model import CollegeModel, VacancyModel, CompanyModel

router = APIRouter(
    prefix="/method",
    tags=["AdminPanel"]
)

#College
@router.get("/api/admin/get_college", summary="Вывод всех колледжей")
async def get_college(session: SessionDepend):
    return await get_setup(session=session, SetupModel=CollegeModel)

@router.post("/api/admin/college/", summary="Добавление колледжей")
async def add_college(college: CollegeSchema, session: SessionDepend):
    direction = ",".join(direction.DirectionName for direction in college.directions) if college.directions else None

    new_college = CollegeModel(
        name=college.name,
        bio=college.bio,
        training_time=college.training_time,
        directions=direction
    )
    session.add(new_college)
    await session.commit()
    return {"detail": "College appended"}

@router.delete("/api/admin/delete_collage/{id_college}", summary="Удаление колледжей")
async def delete_college(id_college: int, session: SessionDepend):
    return await delete_setup(id_setup=id_college, session=session, SetupModel=CollegeModel)



#Vacancies
@router.get("/api/admin/get_vacancies", summary="Вывод всех вакансий")
async def get_vacancies(session: SessionDepend):
    return await get_setup(session=session, SetupModel=VacancyModel)

@router.post("/api/admin/vacancies/", summary="Добавление вакансий")
async def add_vacancies(vacancies: VacancySchema, session: SessionDepend):
    new_vacancies = VacancyModel(
        name=vacancies.name,
        bio=vacancies.bio,
        city=vacancies.city,
        salary=vacancies.salary,
        company_name=vacancies.company_name
    )
    session.add(new_vacancies)
    await session.commit()
    return {"detail": "Vacancies appended"}

@router.delete("/api/admin/delete_vacancy/{id_vacancy}", summary="Удаление вакансий")
async def delete_vacancy(id_college: int, session: SessionDepend):
    return await delete_setup(id_setup=id_college, session=session, SetupModel=CollegeModel)



#Company
@router.get("/api/admin/get_company", summary="Вывод всех компаний")
async def get_company(session: SessionDepend):
    return await get_setup(session=session, SetupModel=CompanyModel)

@router.post("/api/admin/company/", summary="Добавление компаний")
async def add_company(company: CompanySchema, session: SessionDepend):
    new_company = CompanyModel(
        name=company.name,
        target=company.target,
        logo=company.logo,
        contacts=company.contacts,
        type_company=company.type_company,
        quantity=company.quantity
    )
    session.add(new_company)
    await session.commit()
    return {"detail": "Company appended"}

@router.put("/api/admin/update_company/{id_company}", summary="Обновление компании")
async def update_company(id_company: int, company: CompanySchema, session: SessionDepend):
    await update_setup(id_setup=id_company, session=session, SetupModel=CompanyModel)

@router.delete("/api/admin/delete_company/{id_company}", summary="Удаление компаний")
async def delete_company(id_company: int, session: SessionDepend):
    return await delete_setup(id_setup=id_company, session=session, SetupModel=CompanyModel)


#database
@router.post("/api/admin/create_table", summary="setup_databases")
async def setup_databases(session: SessionDepend):
    await setup_database()
    await session.commit()
    return {"detail": "Create table"}

