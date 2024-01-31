from fastapi import APIRouter , File ,Form , UploadFile ,HTTPException
from typing import Annotated
from pydantic import BaseModel


app02 = APIRouter()

class Item(BaseModel):
    name : str
    description : str | None = None
    price : float
    tax : float | None = 10.5


items = {
    'foo':{'name':'Foo','price':50.2},
    'bar':{'name':'Bar','description':'The Bar fighters','price':62,'tax':20.2},
    'baz':{
        'name':'Baz',
        'description':'There goes my baz',
        'price':50.2,
        'tax':10.5,
        }
}

@app02.get('/items/{item_id}')
async def read_item(item_id:str):
    if item_id not in items:
        raise HTTPException(status_code=404,
                            detail='Item not found',
                            headers={"X-Error": "There goes my error"}
                            )
    return {'item':items[item_id]}

@app02.get('/items/{item_id}/name',
           response_model=Item,
           response_model_include=['name','description'])
async def read_item_name(item_id:str):
    return items[item_id]

@app02.get('/items/{item_id}/public',response_model=Item,response_model_exclude=['tax'])
async def read_item_pblic_data(item_id:str):
    return items[item_id]

# -------------------------------------------------------------------------------------

@app02.post('/files/')
async def create_file(
    file:Annotated[bytes,File()],
    fileb:Annotated[UploadFile,File()],
    token:Annotated[str,Form()]
):
    return{
        'file_size':len(file),
        'token':token,
        'fileb_content_type':fileb.content_type
    }