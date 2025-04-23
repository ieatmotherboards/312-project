import os
import hashlib
from pymongo import MongoClient

docker_db = os.environ.get('DOCKER_DB', "false")

if docker_db == "true":
    mongo_client = MongoClient("mongo")
else:
    mongo_client = MongoClient("localhost")


db = mongo_client["312_project"]

users = db["users"]

def get_user_by_hashed_token(hashed_token : str):
    search = users.find_one({"auth_token": hashed_token})
    return search

def get_user_by_username(username : str):
    return users.find_one({"username": username})

def hash_token(token):
    return hashlib.sha256(token.encode()).hexdigest()

def does_username_exist(username : str) -> bool:
    search = get_user_by_username(username)
    if search is None:
        return False
    else:
        return True

def insert_item_by_username(username, item):
    """
    Args: 
        username (string): String representing a username. While you should only call this function after validating if the user exists,
        this function still handlers the error in which username is not found in the db.
        item (string): String representing an item
    Performs db lookup on username and adds the 
    Returns:
        None
    """
    user = get_user_by_username(username=username)
    if user is not None:
        if "inventory" not in user:
            inventory = {item:1}
        else:
            inventory = user['inventory']
            inventory[item] = 1
        users.update_one({"username":username}, {"$set":{"inventory":inventory}})
            
def get_inventory(username: str):
    """
    Args:
        username: string representing a player's username
    Returns:
        Set representing a player's inventory
        None if player doesn't exist
    """
    if not does_username_exist(username=username):
        return None
    lookup = get_user_by_username(username=username)
    if "inventory" not in lookup:
        return {}
    return lookup["inventory"]
    
def get_leaderboard(sort_key: str) -> list:
    """
    Args: 
        sort_key: string representing 
    Returns:
        List of all users sorted on the parameter key
    """
    pass

# def inventory_test():
#     users.insert_one({"username":"backend_testing_1","inventory":{"Axe":1}})
#     app.logger.info("Axe" in get_inventory("backend_testing_1"))

#     users.insert_one({"username":"backend_testing_2"})
#     insert_item_by_username("backend_testing_2","Axe")
    
#     app.logger.info("Axe" in get_inventory("backend_testing_2"))    
   
#     insert_item_by_username("backend_testing_2","Coin")
    
#     app.logger.info("Axe" in get_inventory("backend_testing_2"))
#     app.logger.info("Coin" in get_inventory("backend_testing_2"))