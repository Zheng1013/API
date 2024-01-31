from fastapi import APIRouter ,Body ,Cookie , Header , Response
from fastapi.responses import JSONResponse,RedirectResponse
from typing import Annotated ,Any
from datetime import datetime,time ,timedelta
from uuid import UUID
from pydantic import BaseModel ,EmailStr

app05 = APIRouter()

@app05.put('/items/{item_id}')
async def read_items(
    item_id : UUID,
    start_datetimes : Annotated[datetime | None,Body()] = None,
    end_datetimes :  Annotated[datetime | None , Body()] = None,
    repeat_at : Annotated[time | None,Body()] = None,
    process_after : Annotated[timedelta | None,Body] = None

):
    start_process = start_datetimes + process_after
    duration = end_datetimes - start_process
    return{
        'iten_id':item_id,
        'start_datetimes':start_datetimes,
        'end_datetimes':end_datetimes,
        'repeat_at':repeat_at,
        'process_after':process_after,
        'start_process':start_process,
        'duration':duration
    }

@app05.get('/cookie/')
async def get_cookies(ads_id:Annotated[str|None,Cookie()]= None):
    return {'ads_id':ads_id}

@app05.get('/header/')
async def get_header(user_agent:Annotated[str|None,Header()]=None):
    return {'User-Agent':user_agent}

@app05.get('/xtoken/')
async def get_xtoken(x_token:Annotated[list[str]|None,Header()] = None):
    return {'X-Token values':x_token}

class Item(BaseModel):
    name:str
    description : str | None = None
    price : float 
    tax : float | None = None
    tags : list[str] = []

class UserIn(BaseModel):
    username : str
    password : str
    email : EmailStr
    full_name : str | None = None

class UserOut(BaseModel):
    username : str
    email : EmailStr
    full_name : str | None = None


@app05.post('/items/',response_model=Item)
async def create_item(item:Item) -> Any :
    return item

@app05.get('/items/',response_model=list[Item])
async def read_items() -> Any : 
    return [ 
        Item(name='Portal Gun',price=42.0),
        Item(name='Plumbus',price=32.0)
    ]

# Don't do this in production! 密碼會有洩漏風險
'''
@app05.post("/user/")
async def create_user(user: UserIn) -> UserIn:
    return user
'''

@app05.post("/user/", response_model=UserOut)
async def create_user(user: UserIn) -> Any:
    return user

# ------------------------------------------------------

''' 使用類別繼承的方式 '''

class BaseUser(BaseModel):
    naem : str 
    email :EmailStr
    full_name : str | None = None

class UserIn_1(BaseUser):
    password : str

@app05.post('/user1/')
async def create_user1(user:UserIn_1) -> BaseUser:
    return user

# ------------------------------------------------------
'''
@app05.get('/portal')
async def get_portal(teleport:bool = False ) -> Response :
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return JSONResponse(content={"message": "Here's your interdimensional portal."})
'''

@app05.get('/portal')
async def get_teleport() -> RedirectResponse:
    return RedirectResponse(url= 'https://www.youtube.com/watch?v=dQw4w9WgXcQ')