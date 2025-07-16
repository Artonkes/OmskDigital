from typing import Annotated
from fastapi import Depends

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.DataBase.ConfigDataBase import database_college, post_conn
from app.DataBase.ConfigDataBase import settings

engine = create_async_engine(
    url=post_conn,
    # url=database_college,
    echo=True
)

# print(engine)
new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with new_session() as session:
        yield session

SessionDepend = Annotated[AsyncSession, Depends(get_session)]