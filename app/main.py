import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
import math
from datetime import datetime as dt

receipts = {}

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    shortDescription: str
    price: str

class Receipt(BaseModel):
    retailer: str
    purchaseDate: str
    purchaseTime: str
    total: str
    items: list[Item] = []

'''

'''
@app.get('/receipts/{id}/points', response_description='Get Points')
async def getPoints(id: str):
    if id in receipts:
        return {'points':receipts[id]['points']}
    return {'points':0}

'''
'''
@app.post('/receipts/process')
async def processReceipts(receipt: Receipt):
    print(receipt)
    id = str(uuid.uuid4())
    while True:
        if len(receipts.keys()) > 0:
            if id in receipts:
                id = str(uuid.uuid4())
                continue
            else: break
        else: break
    points = 0
    points += calculatePointsFromName(receipt.retailer)
    points += calculatePointsFromTotal(receipt.total)
    points += calculatePointsFromItems(receipt.items)
    points += calculatePointsFromDate(receipt.purchaseDate)
    points += calculatePointsFromTime(receipt.purchaseTime)
    receipts[id] = {'receipt':receipt, 'points':points}
    return {"id": id}

'''
The below method calculates the points based on the rule:
    - One point for every alphanumeric character in the retailer name.
'''
def calculatePointsFromName(name):
    points = 0
    for letter in name:
        points += 1 if letter.isalnum() else 0
    return points

'''
The below method calculates the points based on the rule:
    - 50 points if the total is a round dollar amount with no cents.
    - 25 points if the total is a multiple of 0.25.
'''
def calculatePointsFromTotal(total):
    total = float(total)
    points += 50 if total % 1 == 0 else 0
    points += 25 if total % 0.25 == 0 else 0
    return points

'''
The below method calculates the points based on the rule:
    - 5 points for every two items on the receipt.
    - If the trimmed length of the item description is a multiple of 3, 
    multiply the price by 0.2 and round up to the nearest integer.
    The result is the number of points earned.
'''
def calculatePointsFromItems(items:list[Item]):
    points = (len(items)//2)*5
    for item in items:
        descLen = len(item.shortDescription.strip())
        if descLen % 3 == 0:
            points += math.ceil(float(item.price)*0.2)
    return points

'''
The below method calculates the points based on the rule:
    - 6 points if the day in the purchase date is odd.
'''
def calculatePointsFromDate(date):
    return 6 if dt.strptime(date,'%Y-%m-%d').day % 2 == 1 else 0

'''
The below method calculates the points based on the rule:
    - 10 points if the time of purchase is after 2:00pm and before 4:00pm.
'''
def calculatePointsFromTime(time):
    time = dt.strptime(time, '%H:%M')
    return 10 if dt.strptime('16:00', '%H:%M') > time and time > dt.strptime('14:00', '%H:%M') else 0




if __name__ == '__main__':
    uvicorn.run(app)

