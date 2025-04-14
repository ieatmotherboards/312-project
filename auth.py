from flask import Flask, request, jsonify

def parse_data():
    '''
    dummy function to pull out username and password from frontend, replace this with actual logic later
    to see how this works on the frontend, check out sendData() in login.html
    '''
    data = request.get_json()
    print("got data")
    js = jsonify({'username': data["username"], "password":data["password"]})
    print(f"got username:{data["username"]} and password:{data["password"]}")
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
    js = jsonify({'username': data["username"], "password": data["password"]})

    return