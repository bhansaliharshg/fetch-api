import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
import math
from datetime import datetime as dt

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Local receipts repository.
receipts = {}

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

'''
THe below method refers to teh endpoint for getting the points.
'''
@app.get('/receipts/{id}/points', response_description='Get Points')
async def get_points(id: str):
    if id:
        id = id.strip()
        if id in receipts:
            return {'points':receipts[id]['points']}
        else:
            return {'points': 0}
    return {'error':'ID is empty.'}

@app.get('/receipts/ids', response_description="Get all IDs")
async def get_all_ids():
    ids = []
    for key, value in receipts.items():
        id = {'id': key, 'receipt': value['receipt'], 'points': value['points']}
        ids.append(id)
    return ids

'''
The below method is the endpoint for processing the receipt. It accepts receipt details in JSON format and calculates the points.
'''
@app.post('/receipts/process')
async def process_receipt(receipt: Receipt):
    #Check if received receipt object is not empty
    if receipt:
        #Generate ID using uuid package
        id = str(uuid.uuid4())

        #Generate a new ID if duplicate ID generated.
        while True:
            if len(receipts.keys()) > 0:
                if id in receipts:
                    id = str(uuid.uuid4())
                    continue
                else: break
            else: break
        
        #Logic to calculate points
        points = 0

        #Check for non emply retailer
        if receipt.retailer:
            #Calculate points for retailer name
            points += calculatePointsFromName(receipt.retailer)
        
        #Check for non empty total
        if receipt.total:
            #Calculate points for total amount
            points += calculatePointsFromTotal(receipt.total)
        
        #Check for non empty items
        if receipt.items:
            #Calculate points for purchased Items
            points += calculatePointsFromItems(receipt.items)
        
        #Check for non empty Purchase Date
        if receipt.purchaseDate:
            #Calculate points for purchased date
            points += calculatePointsFromDate(receipt.purchaseDate)
        
        #Check for non empty Purchase Time
        if receipt.purchaseTime:
            #Calculate points for purchased time
            points += calculatePointsFromTime(receipt.purchaseTime)
        
        #Store receipt and calculated points in local repository(Dictionary)
        receipts[id] = {'receipt':receipt, 'points':points}
        return {"id": id}
    else:
        #Return error if receipt object is empty.
        return {'error': 'Receipts body empty.'}

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
    points = 0
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
        points += math.ceil(float(item.price)*0.2) if len(item.shortDescription.strip()) % 3 == 0 else 0
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

