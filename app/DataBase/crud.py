from sqlalchemy import select, update
from fastapi import HTTPException

from app.DataBase.database import engine
from app.DataBase.Model import Base


async def setup_database():
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)



async def get_setup(session, SetupModel):
    setup = await session.execute(select(SetupModel))
    return setup.scalars().all()


async def delete_setup(id_setup, session, SetupModel):
    try:
        query = select(SetupModel).where(SetupModel.id == id_setup)
        result = await session.execute(query)
        object_setup = result.scalar_one_or_none()
        
        if object_setup is None:
            raise HTTPException(status_code=404, detail=f"Is not found")

        await session.delete(object_setup)
        await session.commit()
        return {"detail": f"{id_setup} delete"}

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Error to delete: {str(e)}")

async def update_setup(id_setup, session, SetupModel):
    result = await session.execute(select(SetupModel).where(SetupModel.id == id_setup))
    setup = result.scalars().first()
