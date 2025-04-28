from src.database import inv_db

def create_inventory(username):
    inv_db.insert_one({'username':username, 'coins':100, 'inventory':[]})

def update_coins(username, coin_change):
    temp=inv_db.find_one({'username':username}, {'_id':0})
    coins= temp['coins'] + coin_change
    inv_db.find_one_and_update({'username':username}, {'$set':{'coins':coins}})

def add_item(username, item):
    temp=inv_db.find_one({'username':username}, {'_id':0})
    cur_inv=temp['inventory']
    cur_inv.append(item)
    inv_db.find_one_and_update({'username':username}, {'$set':{'inventory':cur_inv}})

def check_for_item(username, item):
    user_inv=inv_db.find_one({'username':username}, {'_id':0})
    inventory=user_inv['inventory']
    if item in inventory:
        return True
    else:
        return False
    
def trade(user1, user1_item_list, user2, user2_item_list):
    user1_data=inv_db.find_one({'username':user1}, {'_id':0})
    user2_data=inv_db.find_one({'username':user2}, {'_id':0})
    user1_inv=user1_data['inventory']
    user2_inv=user2_data['inventory']
    for item in user1_item_list:
        user1_inv.remove(item)
        user2_inv.append(item)
    for item in user2_item_list:
        user1_inv.append(item)
        user2_inv.remove(item)
    
    inv_db.find_one_and_update({'username':user1}, {'$set':{'inventory':user1_inv}})
    inv_db.find_one_and_update({'username':user2}, {'$set':{'inventory':user2_inv}})

def buy_item(username, item, cost):
    user_data=inv_db.find_one({'username':username}, {'_id':0})
    user_coins=user_data['coins']
    user_inv=user_data['inventory']
    if user_coins >= cost:
        user_coins=user_coins-cost
        user_inv.append(item)
        inv_db.find_one_and_update({'username':username}, {'$set':{'inventory':user_inv, 'coins':user_coins}})
        return True
    else:
        return False
    
def sell_item(user1, user1_item_list, user2, user2_cost):
    user1_data=inv_db.find_one({'username':user1}, {'_id':0})
    user2_data=inv_db.find_one({'username':user2}, {'_id':0})
    user1_inv=user1_data['inventory']
    user2_inv=user2_data['inventory']
    user1_coins=user1_data['coins']
    user2_coins=user2_data['coins']
    if user2_coins >= user2_cost:
        for item in user1_item_list:
            user1_inv.remove(item)
            user2_inv.append(item)
        user1_coins+=user2_cost
        user2_coins-=user2_cost
        inv_db.find_one_and_update({'username':user1}, {'$set':{'inventory':user1_inv, 'coins':user1_coins}})
        inv_db.find_one_and_update({'username':user2}, {'$set':{'inventory':user2_inv, 'coins':user2_coins}})
        return True
    else:
        return False

def list_inventory(username):
    all_items=inv_db.find_one({'username':username})['inventory']
    return all_items

    
def get_coins(username):
    userdata=inv_db.find_one({'username':username})
    coins=userdata['coins']
    return coins