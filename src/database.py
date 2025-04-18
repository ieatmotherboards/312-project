import os
from pymongo import MongoClient

docker_db = os.environ.get('DOCKER_DB', "false")

if docker_db == "true":
    mongo_client = MongoClient("mongo")
else:
    mongo_client = MongoClient("localhost")


db = mongo_client["312_project"]

users = db["users"]

# testing to see if the database actually works
if __name__ == '__main__':
    users.insert_one({"username": "test", "value": 3})
    find = users.find_one({"username": "test"})
    assert find["value"] == 3   