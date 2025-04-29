from dns.message import make_response

from database import db
from random import randint
from logging import purchase_log

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

    
def loot_box_open():
    random = randint(1,10)

    if random == 10:
        random = randint

    return random

def purchase_loot_box(request):
    cookies = request.cookies

    token = cookies['auth_token']
    hashed_token = db.hash_token(token)

    user = db.get_user_by_hashed_token(hashed_token)

    if user['coins'] < 100:
        purchase_log(user['username'], success=False, message='not logged in')
        return (403, 'not logged in')

    else:
        #Needs to be updated to add to lootboxes
        #Inventory.find_one_and_update({'auth_token': hashed_token}, {'$set': {'coins': user['coins'] - 100, ''}})
        print('')

    purchase_log(user['username'], success=True, message='purchased')
    return (200, '')