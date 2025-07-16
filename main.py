from fastapi import FastAPI
import uvicorn
from app.AdminPanel import AdminRouter

app = FastAPI()

app.include_router(AdminRouter)

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)