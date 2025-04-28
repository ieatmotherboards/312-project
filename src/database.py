import os
import hashlib

from flask import Request
from pymongo import MongoClient

docker_db = os.environ.get('DOCKER_DB', "false")

if docker_db == "true":
    mongo_client = MongoClient("mongo")
else:
    mongo_client = MongoClient("localhost")


db = mongo_client["312_project"]

users = db["users"]
inv_db = db["inventory"]

# users.delete_many({})

def register_user(username : str, password : str):
    db.users.insert_one({
        'username': username,
        'password': password
    })

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

def does_hashed_token_exist(hashed_token : str):
    search = get_user_by_hashed_token(hashed_token)
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

def get_leaderboard(sort_key: str, ascending: bool) -> list:
    """
    Args:
        sort_key: string representing what term to sort users db by, eg "coins", etc
    Returns:
        List of all users sorted on the parameter key
    """
    order = 1 if ascending else -1
    return users.find({}).sort({sort_key:order}).to_list()

def get_coins_leaderboard() -> list:
    """
    Simple function that returns a list of all users with coins, sorted in descending order
    """
    return get_leaderboard("coins", ascending=False)

# def inventory_test():
#     users.insert_one({"username":"backend_testing_1","inventory":{"Axe":1}})
#     app.logger.info("Axe" in get_inventory("backend_testing_1"))

#     users.insert_one({"username":"backend_testing_2"})
#     insert_item_by_username("backend_testing_2","Axe")

#     app.logger.info("Axe" in get_inventory("backend_testing_2"))

#     insert_item_by_username("backend_testing_2","Coin")

#     app.logger.info("Axe" in get_inventory("backend_testing_2"))
#     app.logger.info("Coin" in get_inventory("backend_testing_2"))

# validates request's auth token, returning it hashed if it is valid or returning error codes if invalid
def try_hash_token(request : Request):
    if 'auth_token' not in request.cookies.keys():
        return (None, 'not logged in', 401)
    hashed_token = hash_token(request.cookies['auth_token'])
    if does_hashed_token_exist(hashed_token):
        # success
        return (hashed_token, '', 200)
    else:
        return (None, 'invalid auth token', 401)
