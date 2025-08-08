import os
import shutil
import uuid

from sqlalchemy import select, update
from fastapi import HTTPException

from app.DataBase.Model import CompanyModel, ProjectCompanyModel
from app.DataBase.database import engine
from app.DataBase.Model import Base


async def setup_database():
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()


async def get_setup(session, SetupModel):
    setup = await session.execute(select(SetupModel))
    return setup.scalars().all()


async def upload_img(file, NameDIR, NameSetup):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")

    DIR = f"app/Img Company/{NameSetup}/{NameDIR}"
    os.makedirs(DIR, exist_ok=True)

    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    filename = file.filename
    unique_filename = f"{filename}"
    file_path = os.path.join(DIR, unique_filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    return str(f"app/Img Company/{NameSetup}/{NameDIR}/{unique_filename}")


async def uploads_images(file, NameDIR, NameSetup: str):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")

    DIR = f"app/Img Company/{NameSetup}/{NameDIR}"
    os.makedirs(DIR, exist_ok=True)

    encode_imgs = []
    for file in file:
        filename = file.filename
        unique_filename = f"{filename}"
        file_path = os.path.join(DIR, unique_filename)

        with open(file_path, "wb") as f:
            f.write(await file.read())
            encode_imgs.append(f"app/Img Company/{NameSetup}/{NameDIR}/{unique_filename}")

    return encode_imgs


async def delete_setup(id_setup, session, SetupModel):
    try:
        query = select(SetupModel).where(SetupModel.id == id_setup)
        result = await session.execute(query)
        object_setup = result.scalar_one_or_none()

        if object_setup is None:
            raise HTTPException(status_code=404, detail=f"Id is not found")


        if SetupModel == CompanyModel:

            projects_query = select(ProjectCompanyModel).where(ProjectCompanyModel.id_company == id_setup)

            projects_result = await session.execute(projects_query)
            projects = projects_result.scalars().all()

            for project in projects:
                await session.delete(project)

            company_folder = f"app/Img Company/{object_setup.name}"
            if os.path.exists(company_folder):
                try:
                    shutil.rmtree(company_folder)
                except Exception as folder_error:
                    print(f"Предупреждение: не удалось удалить папку {company_folder}: {folder_error}")

        await session.delete(object_setup)
        await session.commit()

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Error to delete: {str(e)}")


async def update_setup(id_setup, session, SetupModel, setup_schema):
    try:
        result = await session.execute(select(SetupModel).where(SetupModel.id == id_setup))
        obj = result.scalar_one_or_none()

        if obj is None:
            raise HTTPException(status_code=404, detail="Object not found")

        setup_data = setup_schema.dict(exclude_unset=True)
        for key, value in setup_data.items():
            setattr(obj, key, value)

        await session.commit()
        await session.refresh(obj)

        return obj

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Error is {e}")



