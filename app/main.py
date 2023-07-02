import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uuid
from models import Receipt
from helper import Helper

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

#Initialize Helper Class
helper = Helper()

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
        id = str(uuid.uuid3(uuid.NAMESPACE_DNS, str(receipt)))

        #Generate a new ID if duplicate ID generated.
        while True:
            if len(receipts.keys()) > 0:
                if id in receipts:
                    id = str(uuid.uuid3(uuid.NAMESPACE_DNS, str(receipt)))
                    continue
                else: break
            else: break
        
        #Logic to calculate points
        points = 0

        #Check for non emply retailer
        if receipt.retailer:
            #Calculate points for retailer name
            points += helper.calculatePointsFromName(receipt.retailer)
        
        #Check for non empty total
        if receipt.total:
            #Calculate points for total amount
            points += helper.calculatePointsFromTotal(receipt.total)
        
        #Check for non empty items
        if receipt.items:
            #Calculate points for purchased Items
            points += helper.calculatePointsFromItems(receipt.items)
        
        #Check for non empty Purchase Date
        if receipt.purchaseDate:
            #Calculate points for purchased date
            points += helper.calculatePointsFromDate(receipt.purchaseDate)
        
        #Check for non empty Purchase Time
        if receipt.purchaseTime:
            #Calculate points for purchased time
            points += helper.calculatePointsFromTime(receipt.purchaseTime)
        
        #Store receipt and calculated points in local repository(Dictionary)
        receipts[id] = {'receipt':receipt, 'points':points}
        return {"id": id}
    else:
        #Return error if receipt object is empty.
        return {'error': 'Receipts body empty.'}

if __name__ == '__main__':
    uvicorn.run(app)

