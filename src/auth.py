# import requests.cookies
from flask import *
from src.database import users
import bcrypt
import secrets
import hashlib

from src.logging import main_log, auth_log 


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

def register_new_account(request, app):
    data = request.get_json()

    found = users.find_one({'username': data['username']}, {'_id': 0})

    if found is None:
        if validate_password(data['password']):

            salt = bcrypt.gensalt()
            password = bcrypt.hashpw(data['password'].encode(), salt)
            users.insert_one({'username': data['username'], 'password': password.decode(), 'salt': salt.decode()})
            auth_log(username=data['username'], success=True, message='successfully registered', app=app)

            return redirect('/')

        else:
            auth_log(username=data['username'], success=False, message='tried to register but password was not strong enough', app=app)
            return make_response('Invalid Password', 400)
    else:
        auth_log(username=data['username'], success=False, message='tried to register but username was already taken', app=app)
        return make_response('An Account With That Username Already Exists', 400)


def login(request, app):
    data = request.get_json()

    found = users.find_one({'username': data['username']}, {'_id': 0})

    if found is not None:
        salt = found['salt']
        password = bcrypt.hashpw(data['password'].encode(), salt)

        if password.decode() == found['password']:

            token = secrets.token_hex()
            cookie = str(token)

            token = token.encode()
            token = hashlib.sha256(token).hexdigest()
            users.find_one_and_update({'username': data['username']}, {'$set': {'auth_token': str(token)}})

            res = make_response(redirect('/'))
            res.set_cookie('auth_token', cookie, max_age=86400, httponly=True)

            return res

        else:
            return make_response('Incorrect Password', 400)
    else:
        return make_response('No Account With That Name Found', 400)


def logout(request):
    token = request.cookies.get('auth_token')

    token = token.encode()
    token = hashlib.sha256(token).hexdigest()

    found = users.find_one({'auth_token': token}, {'_id': 0})

    if found is not None:
        if token == found['auth_token']:
            users.find_one_and_update({'auth_token': str(token)}, {'$set': {'auth_token': ''}})

            token = secrets.token_hex()
            cookie = str(token)

            res = make_response()
            res.set_cookie('auth_token', cookie, max_age=1, httponly=True)

            return res
        else:
            return make_response(400, 'Bad Request')
    else:
        return make_response(400, 'Not Logged In')
