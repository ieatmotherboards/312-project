# import requests.cookies
from flask import *
from src.init import app
import src.database as db
import bcrypt
import secrets
import hashlib
import src.inventory as inv
import src.achievements as ach
from src.logging_things import main_log, auth_log, logout_log, register_log
import html

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

special_chars = ['!', '@', '#', '$', '%', '^', '&', '(', ')', '=', '-', '_']

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
        elif char in special_chars:
            contains_special = True
        else:
            return False
        if contains_number and contains_special and contains_lower and contains_upper:
            return True
    return False

def register_new_account(request : Request):
    data = request.get_json()

    username = data['username']
    username = html.escape(username)
    password = data['password']

    if not db.does_username_exist(username):
        if validate_password(password):
            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            db.register_user(username, hashed_password)

            register_log(username=username, success=True, message='successfully registered')
            inv.create_inventory(username)
            ach.create_achievements(username)
            return make_response()
        else:
            register_log(username=username, success=False, message='password was not strong enough')
            return make_response('Invalid Password', 400)
    else:
        register_log(username=username, success=False, message='username was already taken')
        return make_response('An Account With That Username Already Exists', 400)


def login(request : Request):
    data = request.get_json()

    username : str = data['username']
    password : str = data['password']

    user = db.get_user_by_username(username)

    if user is not None:
        stored_password : str = user['password']
        if bcrypt.checkpw(password.encode(), stored_password.encode()):
            token = secrets.token_hex()
            hashed_token = db.hash_token(token)

            db.users.update_one({'username': username}, {'$set': {'auth_token': hashed_token}})
            inv.check_inventory(username)
            ach.check_achievements(username)

            auth_log(username=username, success=True, message='successfully logged in')
            return {'auth_token': token}
        else:
            auth_log(username=username, success=False, message='incorrect password')
            return {'error': 'Incorrect Password'}
    else:
        auth_log(username=username, success=False, message='username does not exist')
        return {'error': 'No Account With That Name Found'}


def extract_cookie(cookie_val):
    print(cookie_val)

# returns Flask response, 200 OK or 403
def logout(request : Request):
    cookies = request.cookies

    if 'auth_token' not in cookies:
        logout_log("nonexistent user", success=False, message='not logged in')
        return (403, 'not logged in')

    token = cookies['auth_token']
    hashed_token = db.hash_token(token)

    user = db.get_user_by_hashed_token(hashed_token)

    if user is not None:
        db.users.update_one({'auth_token': hashed_token}, {'$set': {'auth_token': 'LOGGED OUT'}})

        logout_log(username=user['username'], success=True, message='successfully logged out')
        response = make_response("Logout Success", 200)
        response.set_cookie('auth_token', 'logged out', max_age=0, httponly=True)
        return response
    else:
        logout_log("invalid user", success=False, message='invalid auth token')
        return make_response('Invalid Auth Token', 403)
