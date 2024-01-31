from fastapi import APIRouter ,Form ,File ,UploadFile
from pydantic import BaseModel, EmailStr
from typing import Annotated
from fastapi.responses import HTMLResponse

app06 = APIRouter()

# ------------------------------------------------------------
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    pass


class UserInDB(UserBase):
    hashed_password: str


def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db


@app06.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved

# ------------------------------------------------------------

@app06.post('/login')
async def login(username:Annotated[str,Form()],password:Annotated[str,Form()]):
    return{'username':username}  

#--------------------------------------------------------------

@app06.post('/files/')
async def create_file(file:Annotated[bytes| None, File(description='A file read as bytes')]):
    if not file:
        return {'message':'No file sent'}
    return{'file_size': len(file)}

@app06.post('/uploadfile/')
async def create_upload_file(file:Annotated[UploadFile,File(description='A file read as uploadFile')]):
    if not file :
        return {'message':'No uploaded file sent'}
    return{'filename':file.filename}

#--------------------------------------------------------------
# HTMLResponse 类来构建响应。这通常用于生成包含动态数据的 HTML 页面，
# ex: 比如从数据库中检索数据、渲染模板或动态生成页面内容。
'''

@app06.post("/files/")
async def create_files(files: Annotated[list[bytes], File()]):
    return {"file_sizes": [len(file) for file in files]}


@app06.post("/uploadfiles/")
async def create_upload_files(files: list[UploadFile]):
    return {"filenames": [file.filename for file in files]}


@app06.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)

'''
