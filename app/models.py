from pydantic import BaseModel
'''
Python Object for Item
'''
class Item(BaseModel):
    shortDescription: str
    price: str

'''
Python Object for Receipt
'''
class Receipt(BaseModel):
    retailer: str
    purchaseDate: str
    purchaseTime: str
    total: str
    items: list[Item] = []