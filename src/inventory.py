from flask import make_response, jsonify
from src.database import *
import uuid
from src.database import db
from random import randint
from src.logging_things import purchase_log
import src.achievements as ach
from src.init import app

def create_inventory(username):
    inv_db.insert_one({'username': username, 'coins': 25, 'inventory': [],'LootBoxes':0})

def check_inventory(username):
    inv = inv_db.find_one({'username': username})
    if inv is None:
        create_inventory(username)

def get_coins(username):
    inv = inv_db.find_one({'username': username})
    return inv['coins']

def update_coins(username, coin_change):
    inv = inv_db.find_one({'username': username})
    coins = inv['coins'] + coin_change
    inv_db.update_one({'username': username}, {'$set': {'coins': coins}})
    ach.set_get_rich(username)
    ach.set_bankrupt(username)


# maps an item's type to its properties
item_type_map = {
    'AiViolation' : {'name' : 'Academic Integerity Violation', 'imagePath' : 'public/items/AiViolation.png'},
    'Alan' : {'name' : 'Alan Hunt Drop Tables', 'imagePath' : 'public/items/Alan.png'},
    'AO' : {'name' : 'Application Objectives', 'imagePath' : 'public/items/AOTrophy.png'},
    'PostCard' : {'name':"Kris's Casino Post Card",'imagePath' : 'public/items/CasinoPost.png'},
    'ChickenJockey' : {'name' : 'Chicken Jockey', 'imagePath' : 'public/items/ChickenJockey.png'},
    'GoldAlan' : {'name' : 'Golden Alan Hunt Drop Tables', 'imagePath' : 'public/items/GoldAlan.png'},
    'GoldKris' : {'name' : 'Golden Kris Schindler', 'imagePath' : 'public/items/GoldenKris.png'},
    'Jesse' : {'name' : 'Jesse Hartloff', 'imagePath' : 'public/items/Jesse.png'},
    'JetSki' : {'name' : "Kris Schindler's Jet Ski", 'imagePath' : 'public/items/JetSki.png'},
    'Kris' : {'name' : 'Kris Schindler', 'imagePath' : 'public/items/Kris.png'},
    'Linux' : {'name' : 'Linux OS', 'imagePath' : 'public/items/Linux.png'},
    'MasterSword' : {'name' : 'Masterfull Sword', 'imagePath' : 'public/items/MasterSword.png'},
    'Mushroom' : {'name' : 'Power Shroom', 'imagePath' : 'public/items/Mushroom.png'},
    'Paul' : {'name' : 'Paul Dickson', 'imagePath' : 'public/items/Paul.png'},
    'PiazzaPass' : {'name' : '1 Guilt Free Piazza Post Card', 'imagePath' : 'public/items/PiazzaPass.png'},
    'PokeBall' : {'name' : 'Monster Ball', 'imagePath' : 'public/items/PokeBall.png'},
    'PortalGun' : {'name' : 'Doorway Gun', 'imagePath' : 'public/items/PortalGun.png'},
    'RayGun' : {'name' : 'High Speed Photon Blaster', 'imagePath' : 'public/items/RayGun.png'},
    'SegFault' : {'name' : 'Segmentation fault', 'imagePath' : 'public/items/SegFault.png'},
    'Windows' : {'name' : 'Windows OS', 'imagePath' : 'public/items/Windows.png'}
    
}

non_gold_items = ['AiViolation', 
                  'Alan', 
                  'AO', 
                  'PostCard', 
                  'ChickenJockey',
                  'Jesse',
                  'JetSki',
                  'Kris',
                  'Linux',
                  'MasterSword',
                  'Mushroom',
                  'Paul',
                  'PiazzaPass',
                  'PokeBall',
                  'PortalGun',
                  'RayGun',
                  'SegFault',
                  'Windows'
]

gold_items = ['GoldAlan', 'GoldKris']

# creates a new item with a type of item_type. returns it's assigned uuid.
def create_item(item_type):
    item_id = str(uuid.uuid4())
    item_db.insert_one({'id': item_id, 'type': item_type})
    return item_id

# adds a new item of type item_type to user's inventory
def add_item(username, item_type):
    inv = inv_db.find_one({'username': username})
    items = inv['inventory']
    item_id = create_item(item_type)
    items.append(item_id)
    inv_db.update_one({'username': username}, {'$set': {'inventory': items}})
    return

# checks user's inventory for an item with an id of item_id
def check_for_item(username, item_id):
    inv = inv_db.find_one({'username': username})
    items = inv['inventory']
    if item_id in items:
        return True
    else:
        return False

# gets the properties of the item with id item_id
def get_item_properties(item_id):
    item_type = item_db.find_one({'id': item_id})['type']
    return item_type

    


def getLeaderBoard():
    sortedData=inv_db.find().sort('coins', -1).to_list(10)
    ret_list = []
    rank = 1
    for person in sortedData:

        ret_list.append({"rank":rank, 'player':person['username'], 'coins':person['coins'],})
        rank+=1
    return ret_list


# user1_stuff & user2_stuff = {'coins': coins to lose, 'items': list of items to lose}
def trade(user1, user1_stuff, user2, user2_stuff):
    app.logger.info("user1 is:" + user1)
    app.logger.info("user2 is:" + user2)

    app.logger.info("user1 stuff is:" + str(user1_stuff))
    app.logger.info("user2 stuff is:" + str(user2_stuff))

    

    user1_data = inv_db.find_one({'username': user1})
    user2_data = inv_db.find_one({'username': user2})
    user1_inv = user1_data['inventory']
    user2_inv = user2_data['inventory']

    user1_new_coins = user1_data['coins'] - user1_stuff['coins'] + user2_stuff['coins']
    user2_new_coins = user2_data['coins'] - user2_stuff['coins'] + user1_stuff['coins']
    trade_items(user1_inv, user1_stuff['items'], user2_stuff['items'])
    trade_items(user2_inv, user2_stuff['items'], user1_stuff['items'])

    inv_db.update_one({'username': user1}, {'$set': {'inventory': user1_inv, 'coins': user1_new_coins}})
    inv_db.update_one({'username': user2}, {'$set': {'inventory': user2_inv, 'coins': user2_new_coins}})
    return

def trade_items(inv: list[str], items_to_lose: list[str], items_to_gain: list[str]):
    for item_id in items_to_lose:
        inv.remove(item_id)
    for item_id in items_to_gain:
        inv.append(item_id)
    return

def buy_item(username, item, cost):
    user_data = inv_db.find_one({'username': username})
    user_coins = user_data['coins']
    user_inv = user_data['inventory']
    if user_coins >= cost:
        user_coins = user_coins - cost
        user_inv.append(item)
        inv_db.update_one({'username': username}, {'$set': {'inventory': user_inv, 'coins': user_coins}})
        return True
    else:
        return False

def sell_item(user1, user1_item_list, user2, user2_cost):
    user1_data = inv_db.find_one({'username': user1})
    user2_data = inv_db.find_one({'username': user2})
    user1_inv = user1_data['inventory']
    user2_inv = user2_data['inventory']
    user1_coins = user1_data['coins']
    user2_coins = user2_data['coins']
    if user2_coins >= user2_cost:
        for item in user1_item_list:
            user1_inv.remove(item)
            user2_inv.append(item)
        user1_coins += user2_cost
        user2_coins -= user2_cost
        inv_db.update_one({'username': user1}, {'$set': {'inventory': user1_inv, 'coins': user1_coins}})
        inv_db.update_one({'username': user2}, {'$set': {'inventory': user2_inv, 'coins': user2_coins}})
        return True
    else:
        return False

def list_inventory(username):
    all_items = inv_db.find_one({'username': username})['inventory']
    return all_items


def getCoinsAndLootBoxCount(username):
    userData=inv_db.find_one({'username':username})
    out={}
    out['money']=userData['coins']
    out['lootboxes'] = userData['LootBoxes']
    return out

def loot_box_open(request):
    random = randint(1,10)

    # TODO: update this, this is mad unsafe
    token = request.cookies['auth_token']
    hashed_token = hashlib.sha256(token.encode()).hexdigest()

    username = users.find_one({'auth_token': hashed_token}, {'_id': 0})['username']
    lootBoxCount=inv_db.find_one({'username':username})['LootBoxes']-1
    inv_db.find_one_and_update({'username':username},{'$set':{'LootBoxes':lootBoxCount}})

    if random==10:
        item_key = gold_items[randint(0,1)]
    else:
        item_key = non_gold_items[randint(0,len(non_gold_items) - 1)]
    item = item_type_map[item_key]

    # now, insert item into inventory
    add_item(username, item_type=item)

    return make_response(jsonify({"reward":item["name"], "image_path":item["imagePath"]}))



def purchase_loot_box(request):
    cookies = request.cookies


    token = cookies['auth_token']
    hashed_token = hashlib.sha256(token.encode()).hexdigest()

    user = users.find_one({'auth_token': hashed_token}, {'_id': 0})['username']

    inventory = inv_db.find_one({'username': user}, {'_id': 0})

    if inventory['coins'] < 100:
        purchase_log(user, success=False, message='not enough coins')
        return make_response('not enough coins', 403)

    else:
        update_coins(user, -100)

        inv_db.find_one_and_update({'username': user}, {'$set': {'LootBoxes': (inventory['LootBoxes'] + 1)}})

    purchase_log(user, success=True, message='purchased')
    return make_response("OK", 200)

if __name__ == '__main__':
    user1_inventory = ['0', '1', '2']
    user2_inventory = ['3', '4', '5']
    trade_items(user1_inventory, ['1', '2'], ['3'])
    trade_items(user2_inventory, ['3'], ['1', '2'])
    pass