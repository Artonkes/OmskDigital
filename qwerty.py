from typing import List
from fastapi import FastAPI, UploadFile, HTTPException, File, Form
import os
import uuid
import uvicorn
from pydantic import BaseModel

app = FastAPI()

class CompanySchema(BaseModel):
    name: str
    bio_min: str
    bio_max: str
    geo: str
    url_company: str
    contact: str
    type_company: str
    number: int
    off_name: str
    icon_company: str
    use_techn: str

    class Config:
        from_attributes = True

async def img(file: UploadFile):
    DIR = "app/ImgCompany/KJ"
    os.makedirs(DIR, exist_ok=True)

    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    filename = file.filename
    unique_filename = f"{filename}_{uuid.uuid4()}"
    file_path = os.path.join(DIR, unique_filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    return file_path

@app.post("/upload_file/")
async def upload_file(files: List[UploadFile] = File(...)):
    uploaded_files = []
    DIR = "app/Img Company/test"
    os.makedirs(DIR, exist_ok=True)

    for file in files:
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")

        filename = file.filename
        unique_filename = f"{filename}_{uuid.uuid4()}"
        file_path = os.path.join(DIR, unique_filename)

        with open(file_path, "wb") as f:
            f.write(await file.read())

        uploaded_files.append(unique_filename)

    return {"message": "Files uploaded successfully", "filenames": uploaded_files}

if __name__ == '__main__':
    uvicorn.run("qwerty:app", reload=True)