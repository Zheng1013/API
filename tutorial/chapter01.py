from fastapi import APIRouter , Request
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from enum import Enum



app01 = APIRouter()

class Item(BaseModel):
    name : str 
    description : str | None = None
    price : float
    tax : float | None = None
    tags : set[str] = set()

class Tags(Enum):
    items = 'items'
    users = 'users'

class Item(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    tax: float = 10.5
    tags: list[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}
# 範例
''' 
@app01.post('/items/',
            response_model=Item,summary= 'Create an Item',tags= [Tags.items])
async def create_item(item:Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item

@app01.get('/items/',tags = [Tags.items])
async def read_item():
    return [{'name':'foo','price':50.2}]

@app01.get('/user',tags= [Tags.users])
async def read_users():
    return [{'username':'johndoe'}]

'''



@app01.get('/users/{user_id}')
def read_root(user_id:str,request:Request):
    client_host = request.client.host
    return {'client_host':client_host,'item_id':user_id}


@app01.get('/items/{item_id}',response_model=Item)
async def  read_item(item_id:str ):
    return items[item_id]

@app01.patch("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    stored_item_data = items[item_id]
    stored_item_model = Item(**stored_item_data)
    update_data = item.dict(exclude_unset=True)
    updated_item = stored_item_model.copy(update=update_data)
    items[item_id] = jsonable_encoder(updated_item)
    return updated_item