from fastapi import APIRouter , Body
from pydantic import BaseModel , Field 
from typing import Annotated

app04 = APIRouter()

# 第一種寫法
'''
class Item(BaseModel):
    name : str 
    description : str | None = None
    price : float
    tax : float | None = None

    class Config:
        schema_extra = {
            'example':[
                {
                    'name':'Foo',
                    'description':'A very nice Item',
                    'price' : 35.4,
                    'tax' : 3.2,
                }
            ]
        }
'''

# 第二種寫法,直接將範例寫在class裡
'''
class Item(BaseModel):
    name : str = Field(examples=['Foo'])
    description : str | None = Field(default=None,examples=['A very nice Item'])
    price : float = Field(examples=[35.4])
    tax : float | None = Field(default=None,examples=[3.2])

'''

# 第三種普通的class,範例寫在路由裡
class Item(BaseModel):
    name : str 
    description : str | None = None    
    price : float 
    tax : float | None = None
    



@app04.put('/items/{item_id}')
async def update_item(item_id:int , item:Item):
    results = {'item_id':item_id,'item':item}
    return results

# example不寫在class裡,寫在路由裡的Body函數裡ˇ
@app04.put('/items/{item_id}')
async def update_item(
    item_id : int ,
    item :Annotated[
        Item,
        Body(
            examples=[
                {
                    'name':'Foo',
                    'description':'A very nice Item',
                    'price' : 35.4 ,
                    'tax' : 3.2
                }
            ]
        )
        ]
):
    results = {'item_id':item_id,'item':item}
    return results