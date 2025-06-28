from fastapi import FastAPI, HTTPException
import uvicorn

from shema import CollegeShema
from DataBase.crud import setup_database
from DataBase.database import SessionDepend
from DataBase.Model import CollegeModel

app = FastAPI()

@app.post("/api/college", summary="Get_college", tags=["College"])
async def get_college(college: CollegeShema, session: SessionDepend):
    new_college = CollegeModel(
        name=college.name,
        bio=college.bio,
        max_ball=college.max_ball,
        min_ball=college.min_ball,
        paid_places=college.paid_places,
        free_places=college.free_places,
    )
    session.add(new_college)
    await session.commit()
    return {"detail": "College appended"}

@app.post("/create_table")
async def setup_databases():
    await setup_database()
    return {"detail": "Create table"}

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)