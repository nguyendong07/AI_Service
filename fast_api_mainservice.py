from typing import Union

import aiofiles
from fastapi import FastAPI, UploadFile,File
from compare_face import compare
import shutil

app = FastAPI()

db = []

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/uploadfile/compare/")
async def create_upload_file(file: UploadFile = File(), file2: UploadFile = File()):
    with open("destination.png", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    with open("temp.png", "wb") as newbuffer:
        shutil.copyfileobj(file2.file, newbuffer)

    distance = compare("destination.png", "temp.png")
    if distance < 0.45:
        rs = {
            "code": "200",
            "data": {
                "isMatch": "true",
                "similarity": 1 - distance,
                "isBothImgIDCard": "true"
            },
            "message": "request successful.",
        }
    elif distance > 0.45:
        rs = {
            "code": "200",
            "data": {
                "isMatch": "false",
                "similarity": 1 - distance,
                "isBothImgIDCard": "false"
            },
            "message": "request successful.",
        }
    else:
        rs = {
            "code": "400",
            "data": {
                "error": "Something went wrong, make sure both images contain face"
            },
            "message": "request error.",
        }
    return {"result": rs}
