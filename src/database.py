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

# users.delete_many({})

def register_user(username : str, password : str):
    db.users.insert_one({
        'username': username,
        'password': password,
        'coins': 0
    })

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

# testing to see if the database actually works
if __name__ == '__main__':
    users.insert_one({"username": "test", "value": 3})
    find = users.find_one({"username": "test"})
    assert find["value"] == 3   