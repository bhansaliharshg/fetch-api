from datetime import datetime as dt
from models import Item
import math

class Helper:
    '''
    The below method calculates the points based on the rule:
        - One point for every alphanumeric character in the retailer name.
        '''
    def calculatePointsFromName(self, name):
        points = 0
        for letter in name:
            points += 1 if letter.isalnum() else 0
        return points

    '''
    The below method calculates the points based on the rule:
        - 50 points if the total is a round dollar amount with no cents.
        - 25 points if the total is a multiple of 0.25.
    '''
    def calculatePointsFromTotal(self, total):
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
    def calculatePointsFromItems(self, items:list[Item]):
        points = (len(items)//2)*5
        for item in items:
            points += math.ceil(float(item.price)*0.2) if len(item.shortDescription.strip()) % 3 == 0 else 0
        return points

    '''
    The below method calculates the points based on the rule:
        - 6 points if the day in the purchase date is odd.
    '''
    def calculatePointsFromDate(self, date):
        return 6 if dt.strptime(date,'%Y-%m-%d').day % 2 == 1 else 0

    '''
    The below method calculates the points based on the rule:
        - 10 points if the time of purchase is after 2:00pm and before 4:00pm.
    '''
    def calculatePointsFromTime(self, time):
        time = dt.strptime(time, '%H:%M')
        return 10 if dt.strptime('16:00', '%H:%M') > time and time > dt.strptime('14:00', '%H:%M') else 0