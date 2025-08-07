from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import uvicorn

from app.AdminPanel import AdminRouter

app = FastAPI()

app.include_router(AdminRouter)

origins = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)