from flask import *
from database import users
import bcrypt
import uuid
import secrets
import hashlib
import pyotp


def parse_data():
    '''
    dummy function to pull out username and password from frontend, replace this with actual logic later
    to see how this works on the frontend, check out sendData() in login.html
    '''
    data = request.get_json()
    print("got data")
    js = jsonify({'username': data["username"], "password":data["password"]})
    print(f'got username:{data["username"]} and password:{data["password"]}')
    return js



def validate_password(password):
    if len(password) < 8:
        return False

    contains_upper = False
    contains_lower = False
    contains_number = False
    contains_special = False

    for char in password:
        if char.isupper():
            contains_upper = True
        elif char.islower():
            contains_lower = True
        elif char.isnumeric():
            contains_number = True
        elif char == '!' or char == '@' or char == '#' or char == '$' or char == '%' or char == '^' or char == '&' or char == '(' or char == ')' or char == '=' or char == '-' or char == '_':
            contains_special = True
        else:
            return False

    if contains_number and contains_special and contains_lower and contains_upper:
        return True

    return False

def register_new_account():
    data = request.get_json()

    found = users.find_one({'username': data['username']}, {'_id': 0})

    if found is None:
        if validate_password(data['password']):

            salt = bcrypt.gensalt()
            password = bcrypt.hashpw(data['password'].encode(), salt)
            users.insert_one({'username': data['username'], 'password': password.decode(), 'salt': salt.decode()})

            return make_response('OK', 200)

        else:
            return make_response('Invalid Password', 400)
    else:
        return make_response('An Account With That Username Already Exists', 400)


def login():
    data = request.get_json()



    return
