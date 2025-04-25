from src.database import db

from pymongo import MongoClient

Inventory = db["inventory"]


def createInventory(username):
    Inventory.insert_one({'username':username,'coins':100,'inventory':[]})

def updateCoins(username,coinChange):
    temp=Inventory.find({'username':username},{'_id':0})
    coins=temp['coins']+coinChange
    Inventory.find_one_and_update({'username':username},{'$set':{'coins':coins}})

def addItem(username,item):
    temp=Inventory.find({'username':username},{'_id':0})
    curInv=temp['inventory']
    curInv.append(item)
    Inventory.find_one_and_update({'username':username},{'$set':{'inventory':curInv}})

def checkForItem(username,item):
    temp=Inventory.find({'username':username},{'_id':0})
    inventory=temp['inventory']
    if item in inventory:
        return True
    else:
        return False
    
def trade(user1,user1ItemList,user2,user2ItemList):

    user1Data=Inventory.find({'username':user1},{'_id':0})
    user2Data=Inventory.find({'username':user2},{'_id':0})
    user1Inv=user1Data['inventory']
    user2Inv=user2Data['inventory']
    for item in user1ItemList:
        user1Inv.remove(item)
        user2Inv.append(item)
    for item in user2ItemList:
        user1Inv.append(item)
        user2Inv.remove(item)
    
    Inventory.find_one_and_update({'username':user1},{'$set':{'inventory':user1Inv}})
    Inventory.find_one_and_update({'username':user2},{'$set':{'inventory':user2Inv}})

def buyItem(username,item,cost):
    userData=Inventory.find({'username':username},{'_id':0})
    userCoins=userData['coins']
    userInv=userData['inventory']
    if userCoins >= cost:
        userCoins=userCoins-cost
        userInv.append(item)
        Inventory.find_one_and_update({'username':username},{'$set':{'inventory':userInv,'coins':userCoins}})
        return True
    else:
        return False
    
def sellItem(user1,user1ItemList,user2,user2Cost):
    user1Data=Inventory.find({'username':user1},{'_id':0})
    user2Data=Inventory.find({'username':user2},{'_id':0})
    user1Inv=user1Data['inventory']
    user2Inv=user2Data['inventory']
    user1Coins=user1Data['coins']
    user2Coins=user2Data['coins']
    if user2Coins >= user2Cost:
        for item in user1ItemList:
            user1Inv.remove(item)
            user2Inv.append(item)
        user1Coins+=user2Cost
        user2Coins-=user2Cost
        Inventory.find_one_and_update({'username':user1},{'$set':{'inventory':user1Inv,'coins':user1Coins}})
        Inventory.find_one_and_update({'username':user2},{'$set':{'inventory':user2Inv,'coins':user2Coins}})
        return True
    else:
        return False

def listInventory(username):
    allItems=Inventory.find_one({'username':username})['inventory']
    return allItems

    
def getCoins(username):
    userdata=Inventory.find_one({'username':username})
    coins=userdata['coins']
    return coins