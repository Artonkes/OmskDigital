from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
from starlette.staticfiles import StaticFiles

from app.admin import AdminRouter

app = FastAPI()

origins = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    from fastapi.exceptions import HTTPException
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.detail}
        )
    return JSONResponse(
        status_code=500,
        content={"error": f"Unexpected error: {exc}"}
    )
#TODO
# app.mount("/media", StaticFiles(directory=""), name="media")

app.include_router(AdminRouter)

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)