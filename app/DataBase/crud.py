import os
import uuid

from sqlalchemy import select, update
from fastapi import HTTPException

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

async def upload_image(file, NameSetup: str):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")

    DIR = f"app/Img Company/{NameSetup}"
    os.makedirs(DIR, exist_ok=True)

    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    filename = file.filename
    unique_filename = f"{filename}"
    file_path = os.path.join(DIR, unique_filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    return str(f"app/Img Company/{NameSetup}/{unique_filename}")


async def upload_images(file, NameSetup: str):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")

    DIR = f"app/Img Company/{NameSetup}"
    os.makedirs(DIR, exist_ok=True)

    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    filename = file.filename
    unique_filename = f"{filename}"
    file_path = os.path.join(DIR, unique_filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    return str(f"app/Img Company/{NameSetup}/{unique_filename}")


async def delete_setup(id_setup, session, SetupModel):
    try:
        query = select(SetupModel).where(SetupModel.id == id_setup)
        result = await session.execute(query)
        object_setup = result.scalar_one_or_none()
        
        if object_setup is None:
            raise HTTPException(status_code=404, detail=f"Id is not found")

        await session.delete(object_setup)
        await session.commit()
        return {"detail": f"{id_setup} delete"}

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Error to delete: {str(e)}")

async def update_setup(id_setup, session, SetupModel, setup_schema):
    try:
        query = select(SetupModel).where(SetupModel.id == id_setup)
        result = await session.execute(query)
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


