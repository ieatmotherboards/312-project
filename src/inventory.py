from database import db

from pymongo import MongoClient

Inventory = db["inventory"]


def createInventory(username):
    Inventory.insert_one({'username':username,'coins':100,'inventory':[]})

def updateCoins(username,coinChange):
    temp=Inventory.find({'username':username},{'_id':0})
    coins=temp['coins']+coinChange
    Inventory.find_one_and_update({'username':username},{'$set':{'coins':coins}})