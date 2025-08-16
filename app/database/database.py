from typing import Annotated
from fastapi import Depends

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.database.config_database import settings

engine = create_async_engine(
    url=settings.TEST_DATABASE_URL,
    echo=True
)

new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with new_session() as session:
        yield session

SessionDepend = Annotated[AsyncSession, Depends(get_session)]