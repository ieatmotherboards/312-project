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

def does_username_exist(username : str):
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

# testing to see if the database actually works
if __name__ == '__main__':
    users.insert_one({"username": "test", "value": 3})
    find = users.find_one({"username": "test"})
    assert find["value"] == 3   