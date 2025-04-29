from src.database import inv_db, item_db
import uuid

def create_inventory(username):
    inv_db.insert_one({'username': username, 'coins': 100, 'inventory': []})

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


# maps an item's type to its properties
item_type_map = {
    'orb': {'name': 'The Orb', 'imagePath': 'public/items/orb.png'},
    'axe': {'name': "Woodcutter's axe", 'imagePath': 'public/items/axe.png'},
    'alan_drop_tables': {'name': "Alan Hunt Drop Tables (everybody knows what this means)",
                         'imagePath': 'public/items/alan_tables.png'}
}

# creates a new item with a type of item_type. returns it's assigned uuid.
def create_item(item_type):
    item_id = uuid.uuid4()
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
    item_type = item_db.find_one({'id": item_id'})['type']
    return item_type_map[item_type]

<<<<<<< HEAD
    
def getCoins(username):
    userdata=Inventory.find_one({'username':username})
    coins=userdata['coins']
    return coins

def getLeaderBoard():
    soretedData=Inventory.find().sort('coins',1)
    return soretedData

=======

# user1_stuff & user2_stuff = {'coins': coins to lose, 'items': list of items to lose}
def trade(user1, user1_stuff, user2, user2_stuff):
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

if __name__ == '__main__':
    user1_inventory = ['0', '1', '2']
    user2_inventory = ['3', '4', '5']
    trade_items(user1_inventory, ['1', '2'], ['3'])
    trade_items(user2_inventory, ['3'], ['1', '2'])
    pass
>>>>>>> main
