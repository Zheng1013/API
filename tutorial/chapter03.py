from fastapi import APIRouter , Body ,status 
from typing import Annotated 
from pydantic import BaseModel ,HttpUrl 

app03 = APIRouter()

class Image(BaseModel):
    url : HttpUrl
    name : str 

class Item(BaseModel):
    name:str
    description:str | None = None
    price:float
    tax: float | None = None
    tags : set[str] = set()
    image : list[Image] | None = None

class User(BaseModel):
    username: str
    full_name: str | None = None

class Offer(BaseModel):
    name:str
    description: str | None = None
    price : float
    items : list[Item]



'''
@app03.put('/items/{item_id}')
async def update_item(
    item_id : Annotated[int,Path(title="The ID of the item to get",ge=0,le=1000)],
    q:str | None = None , 
    item : Item | None = None
):
    results = {'item_id':item_id}
    if q :
        results.update({'q':q})
    if item:
        results.update({'item':item})
    return results

'''


@app03.post('/items/',response_model=Item,status_code=status.HTTP_201_CREATED)
async def create_item(item:Item):
    return item


@app03.get('/items_image/{item_id}')
async def update_image(item_id:int,item:Item):
    results = {'item_id':item_id,'item':item}
    return results

@app03.post('/offer/')
async def create_offer(offer:Offer):
    return offer

@app03.post('/images/multiple/')
async def create_multiple_images(images:list[Image]):
    return images